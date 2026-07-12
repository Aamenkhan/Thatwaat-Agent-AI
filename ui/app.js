document.addEventListener('DOMContentLoaded', () => {
    const promptInput = document.getElementById('prompt-input');
    const sendBtn = document.getElementById('send-btn');
    const chatHistory = document.getElementById('chat-history');

    // Auto-resize textarea
    promptInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });

    function addMessage(content, isUser = false) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${isUser ? 'user-message' : 'ai-message'}`;
        
        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar';
        avatarDiv.innerHTML = isUser ? '<i class="fa-solid fa-user"></i>' : '<i class="fa-solid fa-robot"></i>';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content glass-panel';
        contentDiv.innerHTML = `<p>${content.replace(/\\n/g, '<br>')}</p>`;
        
        msgDiv.appendChild(avatarDiv);
        msgDiv.appendChild(contentDiv);
        
        chatHistory.appendChild(msgDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    async function sendMessage() {
        const text = promptInput.value.trim();
        if (!text) return;

        // Add user message to UI
        addMessage(text, true);
        promptInput.value = '';
        promptInput.style.height = 'auto';

        // Add loading indicator
        const loadingId = 'loading-' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ai-message`;
        msgDiv.id = loadingId;
        msgDiv.innerHTML = `
            <div class="message-avatar"><i class="fa-solid fa-robot"></i></div>
            <div class="message-content glass-panel">
                <p><i class="fa-solid fa-circle-notch fa-spin"></i> Thinking...</p>
            </div>
        `;
        chatHistory.appendChild(msgDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;

        try {
            // Call Python Backend API
            const response = await fetch('http://127.0.0.1:5000/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: text })
            });
            
            const data = await response.json();
            
            // Remove loading and add response
            document.getElementById(loadingId).remove();
            if (data.reply) {
                addMessage(data.reply, false);
            } else {
                addMessage("Error: Could not get response.", false);
            }
        } catch (error) {
            document.getElementById(loadingId).remove();
            addMessage(`Error connecting to server: ${error.message}`, false);
        }
    }

    sendBtn.addEventListener('click', sendMessage);
    promptInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
});
