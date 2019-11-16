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
        
        const index = [...colorsList.children].indexOf(liElement);
        currentColor = index;

        if (!sizes[index].some(el => el == selectedSize)) {
            const sizeIndex = sizes[index].indexOf(selectedSize);
            if (sizeIndex !== -1) {
                console.warn('lol');
                // Fallback to other size when there is no such size in that color.
                selectedSize = sizes[index][sizeIndex-1] || sizes[index][sizeIndex+1] || null;
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

addToBasketBtn.addEventListener('click', e => {
    e.preventDefault();

    if (!selectedSize) {
        alert('Choose size first!');
    } else if (selectedSize != sizesSelect.value) {
        alert('HEY MAN YOU GOTTA orde rwrong size!!111');
    } else {
        alert('ordered! ( ͡° ͜ʖ ͡°)');
    }
});