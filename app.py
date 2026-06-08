import asyncio
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.ollama import OllamaChatCompletion, OllamaPromptExecutionSettings
from semantic_kernel.contents import ChatHistory

async def main():
    # 1. Initialize Microsoft's Kernel engine
    kernel = Kernel()

    # 2. Add your remote GPU server natively
    remote_gpu_service = OllamaChatCompletion(
        ai_model_id="qwen2.5vl:latest",          
        host="http://10.22.39.192:11434"  
    )
    kernel.add_service(remote_gpu_service)

    # Instantiate execution settings (required by Semantic Kernel)
    execution_settings = OllamaPromptExecutionSettings()

    # 3. Create the multi-agent orchestration loop
    history = ChatHistory()
    
    # Define agent personas
    pm_system_prompt = "You are a Product Manager. Break down user requests into clean functional specifications."
    engineer_system_prompt = "You are a Senior Software Engineer. Implement specifications into clean, production-ready Python code. Only provide the code block."

    # --- Turn 1: Product Manager Agent ---
    user_request = "Create a lightweight local cache utility script in Python."
    print("📋 [Product Manager] Analyzing requirements...")
    
    history.add_system_message(pm_system_prompt)
    history.add_user_message(user_request)
    
    # FIXED: Added settings=execution_settings
    pm_response = await remote_gpu_service.get_chat_message_content(
        chat_history=history, 
        settings=execution_settings,
        kernel=kernel
    )
    print(f"\nPM Specification Output:\n{pm_response}")

    # --- Turn 2: Software Engineer Agent ---
    print("\n💻 [Software Engineer] Writing code based on PM specs...")
    
    # Pass context forward for the Engineer
    history.add_assistant_message(str(pm_response))
    history.add_system_message(engineer_system_prompt)
    history.add_user_message("Generate the complete Python implementation for the specification provided above.")
    
    # FIXED: Added settings=execution_settings
    engineer_response = await remote_gpu_service.get_chat_message_content(
        chat_history=history, 
        settings=execution_settings,
        kernel=kernel
    )
    print(f"\nEngineer Code Output:\n{engineer_response}")

if __name__ == "__main__":
    asyncio.run(main())