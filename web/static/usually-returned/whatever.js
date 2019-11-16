const checkoutBtn = document.querySelector('[name="proceedToRetailCheckout"]');

const chatbotBox = document.querySelector('#chatbot');
checkoutBtn.parentNode.parentNode.insertAdjacentElement('afterend', chatbotBox);
const chatbotOverlay = document.querySelector('.chatbot-overlay');

chatbotOverlay.addEventListener('click', e => {
    hideChatbot();
});

checkoutBtn.addEventListener('click', e => {
    e.preventDefault();

    showChatbot();
    sendIndicator();

    setTimeout(() => {
        sendChat('Hey! Looks like you usually return those kind of products :/', false)
        sendIndicator();
    }, 700);
    setTimeout(() => {
        sendChat('Are you sure you need these?', false)
    }, 2500);
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

let messagesState = [];
let writingIndicator = false;

const sendChat = (message, mine) => {
    if (!mine) {
        messagesState = messagesState.filter(item => !item.indicator);
    }

    messagesState.push({
        message: message,
        mine: mine
    });

    renderMessages();
};

const sendIndicator = () => {
    messagesState.push({indicator: true});

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