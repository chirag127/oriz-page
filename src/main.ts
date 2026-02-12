import './style.css'

// Product data
interface Product {
  name: string
  description: string
  url: string
  aliases?: string[]
  category: 'finance' | 'developer' | 'utility' | 'content' | 'office' | 'media'
  icon: string
}

const products: Product[] = [
  {
    name: 'Fin Suite',
    description: 'Comprehensive financial tools and calculators for personal and business finance management.',
    url: 'https://fin.oriz.in',
    aliases: ['money.oriz.in', 'finance.oriz.in', 'wealth.oriz.in', 'calc.oriz.in', 'capital.oriz.in'],
    category: 'finance',
    icon: '💰'
  },
  {
    name: 'Dev Suite',
    description: 'Essential developer tools and utilities for modern software development workflows.',
    url: 'https://dev.oriz.in',
    aliases: ['sw.oriz.in', 'tech.oriz.in', 'code.oriz.in'],
    category: 'developer',
    icon: '⚡'
  },
  {
    name: 'Velvet',
    description: 'Premium adult content platform with advanced features and secure access.',
    url: '#',
    category: 'content',
    icon: '🎭'
  },
  {
    name: 'Office Suite',
    description: 'Powerful office file management tools for document processing and collaboration.',
    url: '#',
    category: 'office',
    icon: '📄'
  },
  {
    name: 'Pixel',
    description: 'Advanced image processing and manipulation tools for creative professionals.',
    url: '#',
    category: 'media',
    icon: '🎨'
  },
  {
    name: 'Utility Tools',
    description: 'Collection of essential web utilities and applications for everyday tasks.',
    url: 'https://tools.oriz.in',
    aliases: ['apps.oriz.in', 'web.oriz.in'],
    category: 'utility',
    icon: '🛠️'
  }
]

// Render products
function renderProducts(): void {
  const productsGrid = document.getElementById('productsGrid')
  if (!productsGrid) return

  productsGrid.innerHTML = products.map(product => `
    <div class="product-card" data-category="${product.category}">
      <div class="product-icon">${product.icon}</div>
      <h3 class="product-name">${product.name}</h3>
      <p class="product-description">${product.description}</p>
      ${product.aliases ? `
        <div class="product-aliases">
          <small>Also available at:</small>
          ${product.aliases.map(alias => `<span class="alias">${alias}</span>`).join('')}
        </div>
      ` : ''}
      <a href="${product.url}" class="product-link" ${product.url.startsWith('http') ? 'target="_blank" rel="noopener noreferrer"' : ''}>
        ${product.url.startsWith('http') ? 'Visit Site' : 'Coming Soon'}
        ${product.url.startsWith('http') ? '<span class="arrow">→</span>' : ''}
      </a>
    </div>
  `).join('')
}

// Smooth scrolling for navigation links
function initSmoothScroll(): void {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(this: HTMLAnchorElement, e: Event) {
      e.preventDefault()
      const target = document.querySelector(this.getAttribute('href') || '')
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        })
      }
    })
  })
}

// Mobile navigation toggle
function initMobileNav(): void {
  const navToggle = document.querySelector('.nav-toggle')
  const navMenu = document.querySelector('.nav-menu')

  if (navToggle && navMenu) {
    navToggle.addEventListener('click', () => {
      navToggle.classList.toggle('active')
      navMenu.classList.toggle('active')
    })

    // Close menu when clicking on a link
    document.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', () => {
        navToggle.classList.remove('active')
        navMenu.classList.remove('active')
      })
    })
  }
}

// Intersection Observer for scroll animations
function initScrollAnimations(): void {
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-in')
        observer.unobserve(entry.target)
      }
    })
  }, observerOptions)

  // Observe all product cards and sections
  document.querySelectorAll('.product-card, .about-content, .contact-content').forEach(el => {
    observer.observe(el)
  })
}

// Header scroll effect
function initHeaderScroll(): void {
  const header = document.querySelector('.header')
  if (!header) return

  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      header.classList.add('scrolled')
    } else {
      header.classList.remove('scrolled')
    }
  })
}

// Initialize all functionality
function init(): void {
  renderProducts()
  initSmoothScroll()
  initMobileNav()
  initScrollAnimations()
  initHeaderScroll()
}

// Run on DOM ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init)
} else {
  init()
}