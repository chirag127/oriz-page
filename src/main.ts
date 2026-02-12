/**
 * Oriz — Main entry point
 * Handles navigation, smooth scrolling, scroll animations,
 * and header background transitions.
 */
import "./style.css";

/* ─── DOM References ───────────────────────────────────── */
const header = document.getElementById("header") as HTMLElement | null;
const navToggle = document.getElementById("nav-toggle") as HTMLButtonElement | null;
const navMenu = document.getElementById("nav-menu") as HTMLElement | null;
const navLinks = document.querySelectorAll<HTMLAnchorElement>(".nav__link");
const animatedElements = document.querySelectorAll<HTMLElement>(".animate-on-scroll");

/* ─── Mobile Navigation ────────────────────────────────── */

/** Creates and manages the mobile nav overlay */
function createOverlay(): HTMLDivElement {
    const overlay = document.createElement("div");
    overlay.classList.add("nav-overlay");
    document.body.appendChild(overlay);
    overlay.addEventListener("click", closeMenu);
    return overlay;
}

const overlay = createOverlay();

function openMenu(): void {
    navMenu?.classList.add("is-open");
    navToggle?.classList.add("is-active");
    navToggle?.setAttribute("aria-expanded", "true");
    overlay.classList.add("is-visible");
    document.body.style.overflow = "hidden";
}

function closeMenu(): void {
    navMenu?.classList.remove("is-open");
    navToggle?.classList.remove("is-active");
    navToggle?.setAttribute("aria-expanded", "false");
    overlay.classList.remove("is-visible");
    document.body.style.overflow = "";
}

function toggleMenu(): void {
    const isOpen = navMenu?.classList.contains("is-open");
    if (isOpen) {
        closeMenu();
    } else {
        openMenu();
    }
}

navToggle?.addEventListener("click", toggleMenu);

// Close menu when a nav link is clicked
navLinks.forEach((link) => {
    link.addEventListener("click", closeMenu);
});

// Close menu on Escape key
document.addEventListener("keydown", (e: KeyboardEvent) => {
    if (e.key === "Escape") closeMenu();
});

/* ─── Smooth Scrolling ─────────────────────────────────── */
document.querySelectorAll<HTMLAnchorElement>('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", (e: Event) => {
        e.preventDefault();
        const href = (e.currentTarget as HTMLAnchorElement).getAttribute("href");
        if (!href) return;

        const target = document.querySelector(href);
        if (!target) return;

        const headerHeight = header?.offsetHeight ?? 72;
        const targetPosition =
            target.getBoundingClientRect().top + window.scrollY - headerHeight;

        window.scrollTo({
            top: targetPosition,
            behavior: "smooth",
        });
    });
});

/* ─── Header Scroll Effect ─────────────────────────────── */
function handleHeaderScroll(): void {
    if (!header) return;
    if (window.scrollY > 50) {
        header.classList.add("is-scrolled");
    } else {
        header.classList.remove("is-scrolled");
    }
}

window.addEventListener("scroll", handleHeaderScroll, { passive: true });
handleHeaderScroll();

/* ─── Active Nav Link Highlighting ─────────────────────── */
const sections = document.querySelectorAll<HTMLElement>("section[id]");

function highlightActiveNav(): void {
    const scrollY = window.scrollY;
    const headerHeight = header?.offsetHeight ?? 72;

    sections.forEach((section) => {
        const sectionTop = section.offsetTop - headerHeight - 100;
        const sectionHeight = section.offsetHeight;
        const sectionId = section.getAttribute("id");

        if (scrollY >= sectionTop && scrollY < sectionTop + sectionHeight) {
            navLinks.forEach((link) => {
                link.classList.remove("is-active");
                if (link.getAttribute("href") === `#${sectionId}`) {
                    link.classList.add("is-active");
                }
            });
        }
    });
}

window.addEventListener("scroll", highlightActiveNav, { passive: true });
highlightActiveNav();

/* ─── Scroll Animations (IntersectionObserver) ─────────── */
const observerOptions: IntersectionObserverInit = {
    root: null,
    rootMargin: "0px 0px -60px 0px",
    threshold: 0.1,
};

const scrollObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            // Unobserve after animation to save resources
            scrollObserver.unobserve(entry.target);
        }
    });
}, observerOptions);

animatedElements.forEach((el) => scrollObserver.observe(el));

/* ─── Year in Footer (dynamic) ──────────────────────────── */
const yearEl = document.querySelector(".footer__bottom p");
if (yearEl) {
    const year = new Date().getFullYear();
    yearEl.textContent = `© ${year} Oriz. All rights reserved.`;
}
