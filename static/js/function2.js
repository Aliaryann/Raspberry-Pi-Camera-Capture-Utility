function captureImage() {
    console.log("clicked hi")
    fetch('/capture_img') // Sends a request to capture an image
        .then(response => response.json())
        .then(data =>{
            console.log(data)
            displayImagesSorted(); // Refresh and display images sorted after capturing new image
        })
        .catch(error => {
            console.error('Error capturing image:', error);
        });
}

function uploadImage() {
    const input = document.querySelector('input[type="file"]');
    const file = input.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('image', file); // 'image' is the key

        fetch('/upload_image', { // Assuming '/upload_image' is your server endpoint
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            console.log(data); // Log server response
            displayImagesSorted(); // Refresh and display images sorted after upload
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}

function displayImagesSorted() {
    console.log('Fetching images...');
    fetch('/get_images')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(images => {
            console.log('Images fetched:', images);
            const sortedImages = images.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
            console.log('Sorted Images:', sortedImages); // Log sorted images
            const imagesContainer = document.getElementById('images-container');
            if (!imagesContainer) {
                console.error('No images-container element found');
                return;
            }
            imagesContainer.innerHTML = ''; // Clear existing images

            sortedImages.forEach(image => {
                const imgElement = document.createElement('img');
                imgElement.src = image.url;
                imgElement.alt = 'Uploaded Image';
                imgElement.style.maxWidth = '200px'; // Style adjustments
                imgElement.style.maxHeight = '200px'; // Style adjustments
                imgElement.style.margin = '10px'; // Space between images
                imagesContainer.appendChild(imgElement);
            });
        })
        .catch(error => {
            console.error('Error fetching images:', error);
        });
}
// scripts.js

document.addEventListener('DOMContentLoaded', (event) => {
    const menuToggle = document.getElementById('menu-toggle');
    const navbar = document.getElementById('navbar');

    menuToggle.addEventListener('click', () => {
        navbar.classList.toggle('active');
    });
});
