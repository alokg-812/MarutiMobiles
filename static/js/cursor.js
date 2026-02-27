document.addEventListener('DOMContentLoaded', () => {
    const cursor = document.createElement('div');
    const cursorGlow = document.createElement('div');
    
    cursor.classList.add('custom-cursor');
    cursorGlow.classList.add('custom-cursor-glow');
    
    document.body.appendChild(cursor);
    document.body.appendChild(cursorGlow);

    let mouseX = 0;
    let mouseY = 0;
    let cursorX = 0;
    let cursorY = 0;
    let glowX = 0;
    let glowY = 0;

    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    const animate = () => {
        // Smooth interpolation for cursor
        cursorX += (mouseX - cursorX) * 0.15;
        cursorY += (mouseY - cursorY) * 0.15;
        cursor.style.left = `${cursorX}px`;
        cursor.style.top = `${cursorY}px`;

        // Slightly faster glow to create a tail-like or layered effect
        glowX += (mouseX - glowX) * 0.25;
        glowY += (mouseY - glowY) * 0.25;
        cursorGlow.style.left = `${glowX}px`;
        cursorGlow.style.top = `${glowY}px`;

        requestAnimationFrame(animate);
    };

    animate();

    // Hover effects for interactive elements
    const interactiveElements = document.querySelectorAll('button, a, .btn, .nav-link, input, select, textarea');
    
    interactiveElements.forEach((el) => {
        el.addEventListener('mouseenter', () => {
            cursor.classList.add('cursor-hover');
            cursorGlow.style.opacity = '0.5';
        });
        el.addEventListener('mouseleave', () => {
            cursor.classList.remove('cursor-hover');
            cursorGlow.style.opacity = '1';
        });
    });
});
