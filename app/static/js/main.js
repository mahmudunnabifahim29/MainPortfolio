/**
 * Main Portfolio JavaScript
 * Handles interactions, animations, and dynamic content fetching.
 */

document.addEventListener('DOMContentLoaded', () => {
    
    // ── 1. THEME TOGGLE ───────────────────────────────────────────────
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    const htmlEl = document.documentElement;
    
    // Check saved theme or system preference
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme) {
        htmlEl.setAttribute('data-theme', savedTheme);
        updateThemeIcon(savedTheme);
    } else if (!prefersDark) {
        htmlEl.setAttribute('data-theme', 'light');
        updateThemeIcon('light');
    }
    
    themeToggle.addEventListener('click', () => {
        const currentTheme = htmlEl.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        htmlEl.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });
    
    function updateThemeIcon(theme) {
        if (theme === 'dark') {
            themeIcon.className = 'fas fa-sun';
        } else {
            themeIcon.className = 'fas fa-moon';
        }
    }
    
    // ── 2. MOBILE NAVIGATION ──────────────────────────────────────────
    const navBurger = document.getElementById('navBurger');
    const navMenu = document.getElementById('navMenu');
    
    navBurger.addEventListener('click', () => {
        navBurger.classList.toggle('active');
        navMenu.classList.toggle('active');
    });
    
    // Close menu when clicking a link
    document.querySelectorAll('.navbar__link').forEach(link => {
        link.addEventListener('click', () => {
            navBurger.classList.remove('active');
            navMenu.classList.remove('active');
        });
    });
    
    // ── 3. SCROLL EFFECTS (Navbar & Back to Top) ──────────────────────
    const navbar = document.getElementById('navbar');
    const backToTop = document.getElementById('backToTop');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        
        if (window.scrollY > 500) {
            backToTop.classList.add('visible');
        } else {
            backToTop.classList.remove('visible');
        }
    });
    
    backToTop.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    
    // ── 4. SCROLL SPY (Active Nav Links) ──────────────────────────────
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.navbar__link');
    
    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (scrollY >= (sectionTop - 200)) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
    
    // ── 5. INTERSECTION OBSERVER (Scroll Animations) ──────────────────
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };
    
    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                
                // Animate progress bars if in skills section
                if (entry.target.classList.contains('skill-card')) {
                    const bar = entry.target.querySelector('.skill-card__fill');
                    if (bar) {
                        setTimeout(() => {
                            bar.style.width = bar.getAttribute('data-level') + '%';
                        }, 200);
                    }
                }
                
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });
    
    // ── 6. SKILLS TABS ────────────────────────────────────────────────
    const tabBtns = document.querySelectorAll('.skills__tab');
    const tabPanels = document.querySelectorAll('.skills__panel');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all
            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanels.forEach(p => p.classList.remove('active'));
            
            // Add active class to clicked
            btn.classList.add('active');
            const targetId = `panel-${btn.getAttribute('data-tab')}`;
            document.getElementById(targetId).classList.add('active');
        });
    });
    
    // ── 7. TYPEWRITER EFFECT ──────────────────────────────────────────
    const texts = [
        "Full-Stack Developer",
        "Competitive Programmer",
        "Problem Solver",
        "Tech Enthusiast"
    ];
    let count = 0;
    let index = 0;
    let currentText = '';
    let letter = '';
    let isDeleting = false;
    const typeElement = document.getElementById('typewriterText');
    
    if (typeElement) {
        (function type() {
            if (count === texts.length) {
                count = 0;
            }
            currentText = texts[count];
            
            if (isDeleting) {
                letter = currentText.slice(0, --index);
            } else {
                letter = currentText.slice(0, ++index);
            }
            
            typeElement.textContent = letter;
            
            let typeSpeed = 100;
            if (isDeleting) {
                typeSpeed /= 2;
            }
            
            if (!isDeleting && letter.length === currentText.length) {
                typeSpeed = 2000; // Pause at end
                isDeleting = true;
            } else if (isDeleting && letter.length === 0) {
                isDeleting = false;
                count++;
                typeSpeed = 500; // Pause before new word
            }
            
            setTimeout(type, typeSpeed);
        })();
    }
    
    // ── 8. PROJECT MODAL ──────────────────────────────────────────────
    const modal = document.getElementById('projectModal');
    const overlay = document.getElementById('modalOverlay');
    const closeBtn = document.getElementById('modalClose');
    const modalTitle = document.getElementById('modalTitle');
    const modalDesc = document.getElementById('modalDesc');
    const modalTags = document.getElementById('modalTags');
    
    document.querySelectorAll('.project-card__details-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const title = btn.getAttribute('data-title');
            const desc = btn.getAttribute('data-description');
            const techs = btn.getAttribute('data-techs').split(',');
            
            modalTitle.textContent = title;
            modalDesc.textContent = desc;
            
            modalTags.innerHTML = '';
            techs.forEach(tech => {
                if(tech.trim()) {
                    const span = document.createElement('span');
                    span.className = 'project-card__tag';
                    span.textContent = tech.trim();
                    modalTags.appendChild(span);
                }
            });
            
            modal.classList.add('active');
            document.body.style.overflow = 'hidden'; // Prevent scrolling
        });
    });
    
    function closeModal() {
        if(modal) {
            modal.classList.remove('active');
            document.body.style.overflow = '';
        }
    }
    
    if(closeBtn) closeBtn.addEventListener('click', closeModal);
    if(overlay) overlay.addEventListener('click', closeModal);
    
    // ── 9. FETCH GITHUB REPOS (Optional functionality) ────────────────
    const githubReposEl = document.getElementById('githubRepos');
    const githubReposGrid = document.getElementById('githubReposGrid');
    
    if (githubReposEl && githubReposGrid) {
        fetch('/api/github-repos')
            .then(res => res.json())
            .then(data => {
                if (data.repos && data.repos.length > 0) {
                    githubReposEl.style.display = 'block';
                    data.repos.forEach(repo => {
                        const card = document.createElement('div');
                        card.className = 'repo-card';
                        card.innerHTML = `
                            <h4><a href="${repo.html_url}" target="_blank" rel="noopener">${repo.name}</a></h4>
                            <p style="font-size:0.875rem; color:var(--text-secondary); margin:0.5rem 0;">
                                ${repo.description || 'No description provided.'}
                            </p>
                            <div style="display:flex; gap:1rem; font-size:0.875rem; color:var(--text-muted); margin-top:1rem;">
                                ${repo.language ? `<span><i class="fas fa-circle" style="color:var(--accent-primary);font-size:0.5rem;vertical-align:middle;"></i> ${repo.language}</span>` : ''}
                                <span><i class="fas fa-star"></i> ${repo.stargazers_count}</span>
                                <span><i class="fas fa-code-branch"></i> ${repo.forks_count}</span>
                            </div>
                        `;
                        githubReposGrid.appendChild(card);
                    });
                }
            })
            .catch(err => console.error('Error fetching repos:', err));
    }
});
