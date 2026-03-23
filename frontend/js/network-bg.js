// Minimal Blockchain Network Animation using Three.js

const initBackground = () => {
    const canvas = document.getElementById('bg-canvas');
    if (!canvas) {
        console.error("Canvas element #bg-canvas not found.");
        return;
    }

    const scene = new THREE.Scene();
    
    // Camera setup
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 30;

    const renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // Create particles (nodes)
    const particleCount = 100;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);

    for (let i = 0; i < particleCount * 3; i++) {
        positions[i] = (Math.random() - 0.5) * 80;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

    // Material for the nodes
    const material = new THREE.PointsMaterial({
        size: 0.3,
        color: 0x00e676, 
        transparent: true,
        opacity: 0.8
    });

    const particles = new THREE.Points(geometry, material);
    scene.add(particles);

    // Create the wireframe connecting lines
    const lineMaterial = new THREE.LineBasicMaterial({
        color: 0x888888,
        transparent: true,
        opacity: 0.15
    });

    const lineGeometry = new THREE.BufferGeometry();
    const lineMesh = new THREE.LineSegments(lineGeometry, lineMaterial);
    scene.add(lineMesh);

    // Initial Theme Check for Lines
    const isLight = document.documentElement.getAttribute('data-theme') === 'light';
    lineMaterial.color.setHex(isLight ? 0x000000 : 0xffffff);
    lineMaterial.opacity = isLight ? 0.08 : 0.15;

    // Animation loop
    const animate = () => {
        requestAnimationFrame(animate);

        particles.rotation.x += 0.0005;
        particles.rotation.y += 0.001;
        
        lineMesh.rotation.x = particles.rotation.x;
        lineMesh.rotation.y = particles.rotation.y;

        const positions = particles.geometry.attributes.position.array;
        const linePositions = [];

        for (let i = 0; i < particleCount; i++) {
            for (let j = i + 1; j < particleCount; j++) {
                const dx = positions[i * 3] - positions[j * 3];
                const dy = positions[i * 3 + 1] - positions[j * 3 + 1];
                const dz = positions[i * 3 + 2] - positions[j * 3 + 2];
                const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);

                if (dist < 12) {
                    linePositions.push(
                        positions[i * 3], positions[i * 3 + 1], positions[i * 3 + 2],
                        positions[j * 3], positions[j * 3 + 1], positions[j * 3 + 2]
                    );
                }
            }
        }

        lineMesh.geometry.setAttribute('position', new THREE.Float32BufferAttribute(linePositions, 3));
        renderer.render(scene, camera);
    };

    animate();

    // Handle Window Resize
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });

    // Listen for Theme Changes dynamically
    const observer = new MutationObserver(() => {
        const currentLight = document.documentElement.getAttribute('data-theme') === 'light';
        lineMaterial.color.setHex(currentLight ? 0x000000 : 0xffffff);
        lineMaterial.opacity = currentLight ? 0.08 : 0.15;
    });
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
};

document.addEventListener('DOMContentLoaded', initBackground);