


class BlogCard extends HTMLElement {
    constructor() {
        super();
    }

    connectedCallback() {
        // Get properties from attributes or use defaults
        const title = this.getAttribute('title') || 'Blog Title';
        const image = this.getAttribute('image') || '/static/images/default-blog.jpg';
        const category = this.getAttribute('category') || 'Uncategorized';
        const summary = this.getAttribute('summary') || 'No summary available';
        const link = this.getAttribute('link') || '#';
        const isDraft = this.hasAttribute('draft');
        const publishLink = this.getAttribute('publish-link') || '';

        // Create the card structure
        this.innerHTML = `
            <div class="blog-card ${isDraft ? 'draft' : ''}">
                <div class="blog-card-image">
                    <img src="${image}" alt="${title}">
                </div>
                <div class="blog-card-content">
                    <span class="blog-card-category ${category.toLowerCase()}">${category}</span>
                    <h3 class="blog-card-title">${title}</h3>
                    <p class="blog-card-summary">${summary}</p>
                    ${isDraft ? '<div class="blog-card-status"><span class="status draft">Draft</span></div>' : ''}
                    <div class="blog-card-actions">
                        <a href="${link}" class="btn btn-primary">Read More</a>
                        ${isDraft && publishLink ? `<a href="${publishLink}" class="btn btn-secondary">Publish</a>` : ''}
                    </div>
                </div>
            </div>
        `;
    }
}

// Define custom element
customElements.define('blog-card', BlogCard);