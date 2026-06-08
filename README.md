Multi-Agent Software Development Simulator
An open-source multi-agent orchestration workflow built using Microsoft Semantic Kernel. This project simulates a mini software development company by setting up a sequential communication pipeline between a Product Manager agent and a Senior Software Engineer agent.

The entire framework operates 100% locally and privately, routing all AI generation tasks natively to a remote self-hosted GPU server running Ollama.

🏗️ Architecture Design
Instead of relying on an abstract single-prompt loop, this simulator maintains state isolation by passing an evolving ChatHistory object through distinct agent personas.

                  ┌──────────────────────────────┐
                  │      Remote GPU Server       │
                  │  (Ollama: qwen2.5vl:latest)  │
                  └──────────────────────────────┘
                                  ▲
       ┌──────────────────────────┴──────────────────────────┐
       │                                                     │
[User Request] ──> [Product Manager] ──> [Software Engineer] ──> [Final Code]
                     (Builds Spec)          (Builds Script)
Product Manager (PM): Evaluates raw user prompts and builds rigorous functional requirement documents.

Senior Software Engineer: Inherits the PM's specification documents, configures the technical implementation details, and generates clean, executable Python code.

🛠️ Prerequisites
Before executing the simulator, ensure your local workspace and remote infrastructure match the specifications below.

1. Remote GPU Server Configuration
Your remote GPU server must have Ollama active and exposed across your local network layer.

Host Binding: Ollama must be bound to 0.0.0.0 to permit remote API handshakes. Set this variable on your GPU server host environment before initializing the service:

Bash
export OLLAMA_HOST=0.0.0.0
ollama serve
* **Model Manifest:** Ensure your target model is pulled down on the host environment:
  ```bash
  ollama pull qwen2.5vl:latest
2. Local Machine Setup
Install the necessary Python execution layers inside your virtual environment:

Bash
pip install semantic-kernel
🚀 Quick Start
Clone or copy the project files into your local directory.

Open app.py and verify your connection block reflects your remote network topography:

Python
remote_gpu_service = OllamaChatCompletion(
    ai_model_id="qwen2.5vl:latest",          
    host="http://10.22.39.192:11434"  # Replace with your GPU server IP
)
3. Execute the simulator script:
   ```bash
python app.py
📁 File Structure
Plaintext
├── app.py             # Main multi-agent execution pipeline
└── README.md          # System documentation and deployment instructions
🔒 Security & Privacy Advantages
Zero Cloud Bleed: By using Semantic Kernel's native Ollama connectors instead of wrapped ecosystem configurations, no local environment validation checks force transmission back to external third-party servers.

Air-Gapped Capacity: This system is fully capable of running behind custom corporate firewalls and restricted intranets, guaranteeing complete proprietary data security.
