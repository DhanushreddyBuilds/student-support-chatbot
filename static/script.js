document.addEventListener('DOMContentLoaded', () => {
    const chatBody = document.getElementById('chat-body');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const languageSelect = document.getElementById('language');

    // Auto-focus input
    userInput.focus();

    // Send message on Enter
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    sendBtn.addEventListener('click', sendMessage);

    function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;

        // Add User Message
        addMessage(text, 'user');
        userInput.value = '';

        // Show Typing Indicator
        const typingId = showTypingIndicator();

        // API Call
        fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: text,
                language: languageSelect.value
            })
        })
            .then(response => response.json())
            .then(data => {
                removeTypingIndicator(typingId);
                addMessage(data.reply, 'bot');

                // Handle Structured Data (Tables/Lists) if present
                if (data.data) {
                    renderStructuredData(data.data, data.type);
                }
            })
            .catch(error => {
                removeTypingIndicator(typingId);
                addMessage("⚠️ Somewhere, something went wrong. Please try again.", 'bot');
                console.error('Error:', error);
            });
    }

    function addMessage(text, sender) {
        const div = document.createElement('div');
        div.classList.add('message', `${sender}-message`);

        // Convert newlines to breaks
        div.innerHTML = text.replace(/\n/g, '<br>');

        chatBody.appendChild(div);
        scrollToBottom();
    }

    function showTypingIndicator() {
        const id = 'typing-' + Date.now();
        const div = document.createElement('div');
        div.id = id;
        div.classList.add('message', 'bot-message');
        div.innerHTML = '<span class="typing-dots">...</span>';
        chatBody.appendChild(div);
        scrollToBottom();
        return id;
    }

    function removeTypingIndicator(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function scrollToBottom() {
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    function renderStructuredData(data, type) {
        const div = document.createElement('div');
        div.classList.add('message', 'bot-message');
        div.style.width = '100%'; // Full width for tables

        if (type === 'table') {
            let html = '<table style="width:100%; border-collapse: collapse; margin-top:10px;">';
            // Assuming data is list of dicts or objects
            if (data.length > 0) {
                // Header
                html += '<tr>';
                Object.keys(data[0]).forEach(key => {
                    html += `<th style="border:1px solid #ddd; padding:8px; background:#f2f2f2;">${key.toUpperCase()}</th>`;
                });
                html += '</tr>';
                // Rows
                data.forEach(row => {
                    html += '<tr>';
                    Object.values(row).forEach(val => {
                        html += `<td style="border:1px solid #ddd; padding:8px;">${val}</td>`;
                    });
                    html += '</tr>';
                });
            }
            html += '</table>';

            // Add Download Button
            const btnId = 'btn-' + Date.now();
            html += `<button id="${btnId}" style="margin-top:10px; padding:8px 12px; background:#dc3545; color:white; border:none; border-radius:5px; cursor:pointer;">⬇️ Download PDF</button>`;

            div.innerHTML = html;
            chatBody.appendChild(div);

            // Add Event Listener to the button
            setTimeout(() => {
                const btn = document.getElementById(btnId);
                if (btn) {
                    btn.addEventListener('click', () => downloadPDF(data, 'table'));
                }
            }, 100);

        } else if (type === 'list') {
            let html = '<ul style="padding-left: 20px; margin-top:10px;">';
            data.forEach(item => {
                html += `<li style="margin-bottom: 5px;">${item}</li>`;
            });
            html += '</ul>';

            // Add Download Button
            const btnId = 'btn-' + Date.now();
            html += `<button id="${btnId}" style="margin-top:10px; padding:8px 12px; background:#dc3545; color:white; border:none; border-radius:5px; cursor:pointer;">⬇️ Download PDF</button>`;

            div.innerHTML = html;
            chatBody.appendChild(div);

            // Add Event Listener to the button
            setTimeout(() => {
                const btn = document.getElementById(btnId);
                if (btn) {
                    btn.addEventListener('click', () => downloadPDF(data, 'list'));
                }
            }, 100);
        }

        scrollToBottom();
    }

    function downloadPDF(data, type = 'table') {
        if (!data || data.length === 0) return;

        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();

        doc.text("Student Support - Data Export", 14, 15);

        if (type === 'list') {
            let y = 25;
            doc.setFontSize(12);
            data.forEach(item => {
                // Split text to fit page width
                const lines = doc.splitTextToSize(`• ${item}`, 180);
                doc.text(lines, 14, y);
                y += (lines.length * 7); // Adjust spacing based on lines

                // Add new page if needed
                if (y > 280) {
                    doc.addPage();
                    y = 20;
                }
            });
        } else {
            // Table
            const keys = Object.keys(data[0]);
            const head = [keys.map(key => key.toUpperCase())];
            const body = data.map(row => keys.map(key => row[key]));

            doc.autoTable({
                head: head,
                body: body,
                startY: 20,
                theme: 'grid',
                styles: { fontSize: 10, cellPadding: 3 },
                headStyles: { fillColor: [75, 75, 75] }
            });
        }

        doc.save('student_data.pdf');
    }
});
