const API_URL = 'https://junction-retail.herokuapp.com';

const addToBasketBtn = document.querySelector('#add-to-basket');

const chatbotBox = document.querySelector('#chatbot');
addToBasketBtn.parentNode.parentNode.insertAdjacentElement('afterend', chatbotBox);
const chatbotOverlay = document.querySelector('.chatbot-overlay');

let messagesState = [];
let writingIndicator = false;

addToBasketBtn.addEventListener('click', e => {
    e.preventDefault();
    
    showChatbot();
    sendChat('');
});

chatbotOverlay.addEventListener('click', e => {
    hideChatbot();
});

document.querySelector('.chatbot-form').addEventListener('submit', e => {
    e.preventDefault();

    const input = document.querySelector('.chatbot-form input');

    sendChat(input.value, true);
    input.value = '';
})

const showChatbot = () => {
    chatbotBox.classList.remove('chatbot-hidden');
    chatbotOverlay.classList.remove('chatbot-hidden');

    chatbotBox.querySelector('input').focus();
};

const hideChatbot = () => {
    chatbotBox.querySelector('input').blur();

    chatbotBox.classList.add('chatbot-hidden');
    chatbotOverlay.classList.add('chatbot-hidden');
};

const sendChat = (message) => {
    if (message != '') {
        messagesState.push({
            message: message,
            mine: true
        });
        renderMessages();
    }

    const data = new FormData();
    data.append('case_tag', message == '' ? 'price' : '');
    data.append('input', message);
    data.append('size', 0.0);

    fetch(API_URL + '/chat', {
        method: 'POST',
        body: data
    })
        .then(response => response.text())
        .then(message => {
            if (message == '') return;

            messagesState = messagesState.filter(item => !item.indicator);

            messagesState.push({
                message: message,
                mine: false
            });

            renderMessages();
        });

    sendIndicator();
};

const sendIndicator = () => {
    messagesState.push({ indicator: true });

    renderMessages();
};

const renderMessages = () => {
    const messages = chatbotBox.querySelector('.chatbot-messages');
    messages.innerHTML = '';

    messagesState.forEach(message => {
        if (message.indicator) {
            messages.insertAdjacentHTML('beforeend', `<div class="chatbot-message"><img src="https://thumbs.gfycat.com/BlackandwhiteAmusedGilamonster-max-1mb.gif" width="30"></div>`);
            return;
        }

        messages.insertAdjacentHTML('beforeend', `
            <div class="chatbot-message ${message.mine ? 'chatbot-message-mine' : ''}">
                ${message.message}
            </div>
        `);

        messages.scrollTop = 100000000000000;
    });
};