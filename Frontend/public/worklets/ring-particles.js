const TAU = Math.PI * 2;

function clamp(n, a, b) { return Math.max(a, Math.min(b, n)); }
function fract(x) { return x - Math.floor(x); }
function hash(n) { return fract(Math.sin(n) * 43758.5453123); }

function num(v, fallback) {
    if (!v) return fallback;
    const s = String(v).trim();
    const n = parseFloat(s);
    return Number.isFinite(n) ? n : fallback;
}

function str(v, fallback) {
    const s = v ? String(v).trim() : "";
    return s || fallback;
}

class AgRingParticles {
    static get inputProperties() {
        return [
            "--ag-ring-color",
            "--ag-ring-alpha",
            "--ag-ring-count",
            "--ag-ring-radius",
            "--ag-ring-thickness",
            "--ag-ring-tilt",
            "--ag-ring-stretch",
            "--ag-cursor-x",
            "--ag-cursor-y",
            "--ag-time",
        ];
    }

    paint(ctx, geom, props) {
        const w = geom.width;
        const h = geom.height;

        const color = str(props.get("--ag-ring-color"), "#a78bfa");
        const alpha = num(props.get("--ag-ring-alpha"), 0.18);
        const count = Math.max(60, Math.floor(num(props.get("--ag-ring-count"), 900)));

        const radius = num(props.get("--ag-ring-radius"), Math.min(w, h) * 0.32);
        const thickness = num(props.get("--ag-ring-thickness"), 56);
        const tilt = num(props.get("--ag-ring-tilt"), 0.72);
        const stretch = num(props.get("--ag-ring-stretch"), 1.18);

        const cxN = num(props.get("--ag-cursor-x"), 0.5);
        const cyN = num(props.get("--ag-cursor-y"), 0.5);

        const timeMs = num(props.get("--ag-time"), 0);
        const t = timeMs * 0.001;

        const cx = w * (0.5 + (cxN - 0.5) * 0.08);
        const cy = h * (0.5 + (cyN - 0.5) * 0.06);

        ctx.clearRect(0, 0, w, h);
        ctx.save();
        ctx.translate(cx, cy);

        ctx.globalCompositeOperation = "lighter";
        ctx.fillStyle = color;

        // Keep shadow low to avoid perf drops
        ctx.shadowColor = color;
        ctx.shadowBlur = 8;

        const rot = t * 0.35;

        for (let i = 0; i < count; i++) {
            const r1 = hash(i * 12.9898);
            const r2 = hash(i * 78.233);
            const r3 = hash(i * 39.3467);

            const a = TAU * (i / count) + rot + (r2 - 0.5) * 0.02;

            const wave = Math.sin(t * (0.7 + r1 * 1.3) + r2 * 6.0) * 0.5 + 0.5;

            const radJitter = (r1 - 0.5) * thickness;
            const rr = radius + radJitter + wave * 0.35 * thickness;

            const x = Math.cos(a) * rr * stretch;
            const y = Math.sin(a) * rr * tilt;

            const size = 0.35 + r3 * 1.4;
            const aFade = alpha * (0.35 + 0.65 * wave) * (0.55 + 0.45 * (1 - Math.abs(radJitter / thickness)));

            ctx.globalAlpha = clamp(aFade, 0, 1);
            ctx.beginPath();
            ctx.arc(x, y, size, 0, TAU);
            ctx.fill();
        }

        ctx.restore();
    }
}

registerPaint("ag-ring-particles", AgRingParticles);