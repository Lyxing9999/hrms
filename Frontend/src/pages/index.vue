<script setup lang="ts">
definePageMeta({ layout: false });

const year = new Date().getFullYear();
</script>

<template>
  <div class="page">
    <!-- Background -->

    <!-- Top Bar -->
    <header class="top">
      <div class="top-inner">
        <div class="brand">
          <div class="logo-badge">HR</div>
          <div>
            <div class="brand-name">HRMS</div>
            <div class="brand-sub">Human Resource Management System</div>
          </div>
        </div>

        <div class="actions">
          <NuxtLink to="/auth/login" class="btn btn-primary">Portal Login</NuxtLink>
        </div>
      </div>
    </header>

    <!-- Slide / Hero -->
    <main class="slide">
      <div class="slide-inner">
        <div class="kicker">
          <span class="dot"></span>
          Phnom Penh International University • FSIT • Software Engineering
        </div>

        <h1 class="title">
          Human Resource Management System
          <span class="title-accent">(HRMS)</span>
        </h1>

        <p class="subtitle">
          A premium, business-style portal for employee records, attendance, leave management,
          and export-ready reporting — built with modern UI and secure access.
        </p>

        <div class="cta-row">
          <NuxtLink to="/auth/login" class="btn btn-primary btn-lg">Enter Portal</NuxtLink>
          <a href="#info" class="btn btn-ghost btn-lg">Project Info</a>
        </div>

        <!-- Slide KPI Row -->
        <div class="kpis">
          <div class="kpi">
            <div class="kpi-top">Security</div>
            <div class="kpi-big">RBAC</div>
            <div class="kpi-sub">Role-based access</div>
          </div>
          <div class="kpi">
            <div class="kpi-top">Workflow</div>
            <div class="kpi-big">Fast</div>
            <div class="kpi-sub">Clean UX for HR</div>
          </div>
          <div class="kpi">
            <div class="kpi-top">Output</div>
            <div class="kpi-big">Reports</div>
            <div class="kpi-sub">Export-ready</div>
          </div>
        </div>

        <!-- Slide Footer Card -->
        <section id="info" class="info-card">
          <div class="info-left">
            <div class="info-title">Academic Project</div>
            <div class="info-text">
              <div class="info-line"><b>Year:</b> 2026</div>
              <div class="info-line">
                <b>Faculty:</b> Faculty of Science and Information Technology (FSIT)
              </div>
              <div class="info-line"><b>Department:</b> Software Engineering</div>
              <div class="info-line"><b>Supervisor:</b> Dr. Tan Seryvuth</div>
            </div>
          </div>

          <div class="info-right">
            <div class="members-title">Group Member 4</div>
            <ul class="members">
              <li class="member">
                <span class="member-name">1. Kain Bunly</span>
                <span class="member-id">ID: CSE</span>
              </li>
              <li class="member">
                <span class="member-name">2. San Lyyou</span>
                <span class="member-id">ID: CSE</span>
              </li>
              <li class="member">
                <span class="member-name">3. Sue Theara</span>
                <span class="member-id">ID: MIS2024220028</span>
              </li>
              <li class="member">
                <span class="member-name">4. Yim EangVeng</span>
                <span class="member-id">ID: CSE2024220007</span>
              </li>
              <li class="member">
                <span class="member-name">5. Va Ratana</span>
                <span class="member-id">ID: CSE</span>
              </li>
              <li class="member">
                <span class="member-name">6. Sareth Ratanak</span>
                <span class="member-id">ID: CSE</span>
              </li>
            </ul>
          </div>
        </section>

        <footer class="footer">
          <div>© {{ year }} HRMS • Phnom Penh International University</div>
          <div class="footer-links">
            <NuxtLink to="/auth/login" class="footer-link">Portal</NuxtLink>
            <a href="#info" class="footer-link">Project Info</a>
          </div>
        </footer>
      </div>
    </main>
  </div>
</template>

<style scoped>
.page {
  min-height: 100vh;
  position: relative;
  isolation: isolate;
  color: rgba(255, 255, 255, 0.92);
}

/* Top bar */
.top {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 10;
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  background: color-mix(in srgb, rgba(10, 14, 26, 0.52) 70%, transparent);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}
.top-inner {
  max-width: 1140px;
  margin: 0 auto;
  padding: 14px 18px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}
.brand {
  display: flex;
  align-items: center;
  gap: 12px;
}
.logo-badge {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: grid;
  place-items: center;
  font-weight: 900;
  letter-spacing: 0.6px;
  background: linear-gradient(135deg, rgba(124, 58, 237, 0.95), rgba(34, 211, 238, 0.9));
  box-shadow: 0 14px 30px rgba(124, 58, 237, 0.25);
}
.brand-name {
  font-weight: 900;
  font-size: 14px;
}
.brand-sub {
  font-size: 12px;
  opacity: 0.72;
}

/* Slide */
.slide {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 100px 18px 40px;
}
.slide-inner {
  width: 100%;
  max-width: 1140px;
}

.kicker {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.10);
  background: rgba(255, 255, 255, 0.06);
  font-weight: 800;
  font-size: 12px;
  letter-spacing: 0.2px;
  width: fit-content;
}
.dot {
  width: 9px;
  height: 9px;
  border-radius: 999px;
  background: rgba(34, 211, 238, 0.95);
  box-shadow: 0 0 18px rgba(34, 211, 238, 0.5);
}

.title {
  margin: 18px 0 10px;
  font-size: 54px;
  line-height: 1.04;
  font-weight: 950;
  letter-spacing: -0.8px;
}
.title-accent {
  opacity: 0.78;
  font-weight: 900;
}
@media (max-width: 720px) {
  .title {
    font-size: 38px;
  }
}

.subtitle {
  margin-top: 10px;
  opacity: 0.82;
  font-size: 15px;
  line-height: 1.7;
  max-width: 68ch;
}

.cta-row {
  display: flex;
  gap: 12px;
  margin-top: 18px;
  flex-wrap: wrap;
}

/* KPIs */
.kpis {
  margin-top: 20px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
}
@media (max-width: 980px) {
  .kpis {
    grid-template-columns: 1fr;
  }
}
.kpi {
  padding: 16px;
  border-radius: 18px;
  border: 1px solid rgba(255, 255, 255, 0.10);
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
}
.kpi-top {
  font-size: 12px;
  font-weight: 800;
  opacity: 0.8;
}
.kpi-big {
  margin-top: 8px;
  font-size: 26px;
  font-weight: 950;
  letter-spacing: -0.3px;
}
.kpi-sub {
  margin-top: 4px;
  font-size: 12px;
  opacity: 0.75;
  font-weight: 700;
}

/* Info card */
.info-card {
  margin-top: 18px;
  border-radius: 18px;
  padding: 18px;
  background: color-mix(in srgb, rgba(255, 255, 255, 0.08) 70%, transparent);
  border: 1px solid rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  box-shadow:
    0 24px 70px rgba(0, 0, 0, 0.55),
    0 1px 0 rgba(255, 255, 255, 0.06) inset;
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 14px;
}
@media (max-width: 980px) {
  .info-card {
    grid-template-columns: 1fr;
  }
}
.info-title {
  font-weight: 950;
  margin-bottom: 10px;
}
.info-line {
  margin-top: 6px;
  opacity: 0.86;
  line-height: 1.6;
}

.members-title {
  font-weight: 950;
  margin-bottom: 10px;
}
.members {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 8px;
}
.member {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 10px 12px;
  border-radius: 14px;
  background: rgba(0, 0, 0, 0.16);
  border: 1px solid rgba(255, 255, 255, 0.08);
}
.member-name {
  font-weight: 900;
}
.member-id {
  opacity: 0.75;
  font-weight: 700;
  font-size: 12px;
}

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 10px 14px;
  border-radius: 12px;
  font-weight: 900;
  text-decoration: none;
  border: 1px solid rgba(255, 255, 255, 0.12);
  transition: transform 180ms ease, background 180ms ease, opacity 180ms ease;
}
.btn:hover {
  transform: translateY(-0.5px);
}
.btn:active {
  transform: translateY(0px);
}
.btn-lg {
  padding: 12px 16px;
  border-radius: 14px;
}
.btn-primary {
  color: #fff;
  background: linear-gradient(
    135deg,
    rgba(124, 58, 237, 0.95),
    rgba(34, 211, 238, 0.75)
  );
  border: 1px solid rgba(124, 58, 237, 0.35);
  box-shadow: 0 16px 32px rgba(124, 58, 237, 0.18);
}
.btn-ghost {
  color: rgba(255, 255, 255, 0.9);
  background: rgba(255, 255, 255, 0.06);
}

/* Footer */
.footer {
  margin-top: 18px;
  padding-top: 14px;
  display: flex;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  opacity: 0.86;
  font-weight: 700;
}
.footer-links {
  display: flex;
  gap: 14px;
}
.footer-link {
  color: rgba(255, 255, 255, 0.86);
  text-decoration: none;
}
.footer-link:hover {
  opacity: 1;
}
</style>