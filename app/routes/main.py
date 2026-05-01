"""
Main routes — serves the portfolio landing page.
"""

import requests
from flask import Blueprint, render_template, current_app

main_bp = Blueprint('main', __name__)


# ──────────────────────────────────────────────
#  Static data (used when DB projects are empty)
# ──────────────────────────────────────────────
DEFAULT_PROJECTS = [
    {
        'title': 'To-Do Notes App',
        'description': (
            'A full-featured task management application built with Python and Tkinter. '
            'Includes task creation, deletion, completion tracking, and a time-based '
            'reminder system with alerts. Features a simple and user-friendly GUI.'
        ),
        'technologies': 'Python,Tkinter,SQLite',
        'icon': 'fas fa-check-circle',
        'tech_list': ['Python', 'Tkinter', 'SQLite'],
    },
    {
        'title': 'JavaFX Unit & Currency Converter',
        'description': (
            'Multi-functional converter supporting length, weight, temperature and more. '
            'Integrates real-time currency conversion via online APIs for USD, EUR, GBP, BDT, etc. '
            'Features dynamic responsive UI, input validation, error handling, and clean OOP design.'
        ),
        'technologies': 'Java,JavaFX,REST API,OOP',
        'icon': 'fas fa-exchange-alt',
        'tech_list': ['Java', 'JavaFX', 'REST API', 'OOP'],
    },
    {
        'title': 'Cryptography Project',
        'description': (
            'Implementation of encryption algorithms in C. Demonstrates understanding of '
            'basic cryptographic concepts including symmetric and asymmetric encryption. '
            'CLI-based secure message handling for encoding and decoding.'
        ),
        'technologies': 'C,Cryptography,CLI,Algorithms',
        'icon': 'fas fa-lock',
        'tech_list': ['C', 'Cryptography', 'CLI', 'Algorithms'],
    },
]

SKILLS = {
    'languages': [
        {'name': 'Python', 'level': 85, 'icon': 'fab fa-python'},
        {'name': 'C++', 'level': 80, 'icon': 'fas fa-code'},
        {'name': 'Java', 'level': 75, 'icon': 'fab fa-java'},
        {'name': 'JavaScript', 'level': 70, 'icon': 'fab fa-js-square'},
        {'name': 'C', 'level': 75, 'icon': 'fas fa-microchip'},
    ],
    'web': [
        {'name': 'HTML5', 'level': 90, 'icon': 'fab fa-html5'},
        {'name': 'CSS3', 'level': 85, 'icon': 'fab fa-css3-alt'},
        {'name': 'React', 'level': 55, 'icon': 'fab fa-react'},
        {'name': 'Flask', 'level': 80, 'icon': 'fas fa-flask'},
        {'name': 'Node.js', 'level': 60, 'icon': 'fab fa-node-js'},
    ],
    'tools': [
        {'name': 'Git & GitHub', 'level': 80, 'icon': 'fab fa-git-alt'},
        {'name': 'VS Code', 'level': 90, 'icon': 'fas fa-laptop-code'},
        {'name': 'MongoDB', 'level': 55, 'icon': 'fas fa-database'},
        {'name': 'REST APIs', 'level': 78, 'icon': 'fas fa-plug'},
        {'name': 'Linux CLI', 'level': 65, 'icon': 'fab fa-linux'},
    ],
    'concepts': [
        {'name': 'DSA', 'level': 85, 'icon': 'fas fa-project-diagram'},
        {'name': 'OOP', 'level': 88, 'icon': 'fas fa-cubes'},
        {'name': 'Problem Solving', 'level': 90, 'icon': 'fas fa-brain'},
        {'name': 'MERN Stack', 'level': 55, 'icon': 'fas fa-layer-group'},
    ],
}

TIMELINE = [
    {
        'year': '2022',
        'title': 'Started B.Sc. in CSE',
        'description': 'Began studying Computer Science and Engineering at Mawlana Bhashani Science and Technology University.',
        'icon': 'fas fa-university',
    },
    {
        'year': '2023',
        'title': 'Competitive Programming',
        'description': 'Started solving problems on Codeforces and strengthened algorithmic thinking.',
        'icon': 'fas fa-trophy',
    },
    {
        'year': '2024',
        'title': 'Full-Stack Development',
        'description': 'Explored Flask, MERN stack, and built real-world projects like the To-Do app and converters.',
        'icon': 'fas fa-code',
    },
    {
        'year': '2025–Present',
        'title': '4th Year & Beyond',
        'description': 'Focusing on scalable systems, open-source contributions, and professional software engineering.',
        'icon': 'fas fa-rocket',
    },
]


@main_bp.route('/')
def index():
    """Render the main portfolio page."""
    from app.models.models import Project

    # Use DB projects if any exist, otherwise fall back to defaults
    db_projects = Project.query.filter_by(is_featured=True).order_by(Project.sort_order).all()
    projects = db_projects if db_projects else DEFAULT_PROJECTS

    return render_template(
        'index.html',
        projects=projects,
        skills=SKILLS,
        timeline=TIMELINE,
    )


@main_bp.route('/api/github-repos')
def github_repos():
    """Proxy endpoint to fetch GitHub repos (avoids CORS issues)."""
    username = current_app.config.get('GITHUB_USERNAME', 'fahim')
    try:
        resp = requests.get(
            f'https://api.github.com/users/{username}/repos',
            params={'sort': 'updated', 'per_page': 6},
            timeout=5,
        )
        resp.raise_for_status()
        repos = resp.json()
        data = [
            {
                'name': r['name'],
                'description': r.get('description', ''),
                'html_url': r['html_url'],
                'language': r.get('language', ''),
                'stargazers_count': r.get('stargazers_count', 0),
                'forks_count': r.get('forks_count', 0),
            }
            for r in repos
        ]
        return {'repos': data}
    except Exception as exc:
        current_app.logger.warning(f'GitHub API error: {exc}')
        return {'repos': [], 'error': str(exc)}, 200
