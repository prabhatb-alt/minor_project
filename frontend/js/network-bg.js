// Enhanced Three.js Network Animation with Performance Optimizations

document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("bg-canvas");
    if (!canvas || !window.THREE) return;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });

    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // Limits pixel ratio for performance

    // --- CONFIGURATION (Cranked up for better visuals) ---
    const particleCount = window.innerWidth < 768 ? 90 : 200; // Increased node density
    const maxDistance = 2.0; // Increased connection reach for more web-lines
    const baseSpeed = 0.0015; // Global rotation speed
    const floatSpeed = 0.012; // Individual node drifting speed

    // --- DYNAMIC THEME COLORS ---
    const getColors = () => {
        const isLight = document.documentElement.getAttribute('data-theme') === 'light';
        return {
            particle: isLight ? 0x00c853 : 0x00e676, // Credlytic Green
            line: isLight ? 0x00c853 : 0x00e676,
            lineOpacity: isLight ? 0.20 : 0.35 // Slightly more visible lines
        };
    };

    let colors = getColors();

    // Generate Particles
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const velocities = [];

    for (let i = 0; i < particleCount * 3; i += 3) {
        // Spread particles across a wider 3D space
        positions[i] = (Math.random() - 0.5) * 18;     // X
        positions[i + 1] = (Math.random() - 0.5) * 18; // Y
        positions[i + 2] = (Math.random() - 0.5) * 18; // Z

        velocities.push({
            x: (Math.random() - 0.5) * floatSpeed,
            y: (Math.random() - 0.5) * floatSpeed,
            z: (Math.random() - 0.5) * floatSpeed
        });
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

    const material = new THREE.PointsMaterial({
        color: colors.particle,
        size: 0.06,
        transparent: true,
        opacity: 0.9
    });

    const particles = new THREE.Points(geometry, material);
    scene.add(particles);

    // Generate Lines
    const lineMaterial = new THREE.LineBasicMaterial({
        color: colors.line,
        transparent: true,
        opacity: colors.lineOpacity
    });

    const lineGeometry = new THREE.BufferGeometry();
    const lineMesh = new THREE.LineSegments(lineGeometry, lineMaterial);
    scene.add(lineMesh);

    camera.position.z = 6;

    // --- MOUSE INTERACTION ---
    let mouseX = 0;
    let mouseY = 0;
    let targetX = 0;
    let targetY = 0;
    const windowHalfX = window.innerWidth / 2;
    const windowHalfY = window.innerHeight / 2;

    document.addEventListener('mousemove', (event) => {
        mouseX = (event.clientX - windowHalfX) * 0.001;
        mouseY = (event.clientY - windowHalfY) * 0.001;
    });

    // --- PERFORMANCE OPTIMIZATION (Battery Saver) ---
    let isVisible = true;
    
    // Pause animation when tab is not active
    document.addEventListener("visibilitychange", () => {
        isVisible = !document.hidden;
    });

    // Handle Window Resize seamlessly
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });

    // --- RENDER LOOP ---
    function animate() {
        requestAnimationFrame(animate);

        // CPU Saver: Don't calculate math if the user isn't looking at the page!
        if (!isVisible) return; 

        // 1. Smooth mouse follow (Network tilts towards cursor)
        targetX = mouseX * 0.8;
        targetY = mouseY * 0.8;
        scene.rotation.x += 0.05 * (targetY - scene.rotation.x) + baseSpeed;
        scene.rotation.y += 0.05 * (targetX - scene.rotation.y) + baseSpeed;

        // 2. Move individual particles
        const positions = particles.geometry.attributes.position.array;
        
        for(let i = 0; i < particleCount; i++) {
            const i3 = i * 3;
            positions[i3] += velocities[i].x;
            positions[i3+1] += velocities[i].y;
            positions[i3+2] += velocities[i].z;

            // Bounce off invisible walls to keep them on screen
            if(Math.abs(positions[i3]) > 9) velocities[i].x *= -1;
            if(Math.abs(positions[i3+1]) > 9) velocities[i].y *= -1;
            if(Math.abs(positions[i3+2]) > 9) velocities[i].z *= -1;
        }
        particles.geometry.attributes.position.needsUpdate = true;

        // 3. Draw connecting lines dynamically
        const linePositions = [];
        for (let i = 0; i < particleCount; i++) {
            for (let j = i + 1; j < particleCount; j++) {
                const dx = positions[i * 3] - positions[j * 3];
                const dy = positions[i * 3 + 1] - positions[j * 3 + 1];
                const dz = positions[i * 3 + 2] - positions[j * 3 + 2];
                const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);

                // If particles are close enough, draw a line between them
                if (dist < maxDistance) {
                    linePositions.push(
                        positions[i * 3], positions[i * 3 + 1], positions[i * 3 + 2],
                        positions[j * 3], positions[j * 3 + 1], positions[j * 3 + 2]
                    );
                }
            }
        }

        lineMesh.geometry.setAttribute('position', new THREE.Float32BufferAttribute(linePositions, 3));
        
        // 4. Live Theme Detection Check
        const newColors = getColors();
        if (material.color.getHex() !== newColors.particle) {
            material.color.setHex(newColors.particle);
            lineMaterial.color.setHex(newColors.line);
            lineMaterial.opacity = newColors.lineOpacity;
        }

        renderer.render(scene, camera);
    }

    animate();
});