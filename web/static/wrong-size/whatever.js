const API_URL = 'https://junction-retail.herokuapp.com';

let currentColor = 0;
let selectedSize;

const sizesSelect = document.querySelector('#size-select');
const colorsList = document.querySelector('#color-select');

(function () {
    const sizes = [
        [5, 6, 7, 8],
        [5, 7, 9]
    ];

    const images = [
        'https://images-na.ssl-images-amazon.com/images/I/61-o2BCVzgL._SY500._SX._UX._SY._UY_.jpg',
        'https://images-na.ssl-images-amazon.com/images/I/81AoRZGmqsL._SX500._SX._UX._SY._UY_.jpg'
    ];

    const thumbnailImg = document.querySelector('.item.imageThumbnail img');
    const bigImg = document.querySelector('.item.image img');

    colorsList.addEventListener('click', e => {
        if (e.target.tagName.toLowerCase() != 'img') {
            return;
        }
        
        // 9th ascendant
        const liElement = e.target.parentNode.parentNode.parentNode
            .parentNode.parentNode.parentNode.parentNode.parentNode.parentNode;
        
        const oldIndex = currentColor;
        const index = [...colorsList.children].indexOf(liElement);
        currentColor = index;

        if (!sizes[index].some(el => el == selectedSize)) {
            const sizeIndex = sizes[oldIndex].indexOf(selectedSize);
            if (sizeIndex !== -1) {
                console.warn('lol');
                // Fallback to other size when there is no such size in that color.
                selectedSize = sizes[index][sizeIndex-1] || sizes[index][sizeIndex+1] || sizes[index][0];
            }
        }

        render();
    });

    sizesSelect.addEventListener('input', e => {
        selectedSize = e.target.value;
    })

    const render = () => {
        // Render sizes
        sizesSelect.innerHTML = '<option>Select</option>';
        sizes[currentColor].forEach(size => {
            sizesSelect.insertAdjacentHTML('beforeend', `
                <option value="${size}" ${size == selectedSize ? 'selected' : ''}>${size}</option>
            `)
        });

        thumbnailImg.src = images[currentColor];
        bigImg.src = images[currentColor];

        // Render selected color
        [...colorsList.children].forEach((child, i) => {
            if (currentColor == i) {
                child.classList.add('swatchSelect');
            } else {
                child.classList.remove('swatchSelect');
            }
        });
    };

    render();
})();

const addToBasketBtn = document.querySelector('#add-to-basket');

const chatbotBox = document.querySelector('#chatbot');
addToBasketBtn.parentNode.parentNode.insertAdjacentElement('afterend', chatbotBox);
const chatbotOverlay = document.querySelector('.chatbot-overlay');

let messagesState = [];
let writingIndicator = false;

chatbotOverlay.addEventListener('click', e => {
    hideChatbot();
});

addToBasketBtn.addEventListener('click', e => {
    e.preventDefault();
    
    showChatbot();
    sendChat('');
});

document.querySelector('.chatbot-form').addEventListener('submit', e => {
    e.preventDefault();

    const input = document.querySelector('.chatbot-form input');

    sendChat(input.value, true);
    input.value = '';
})

const sendChat = (message) => {
    if (message != '') {
        messagesState.push({
            message: message,
            mine: true
        });
        renderMessages();
    }

    const data = new FormData();
    data.append('case_tag', message == '' ? 'size' : '');
    data.append('input', message);
    data.append('size', parseFloat(selectedSize));

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