from flask import (
    Flask,
    render_template_string,
    redirect,
    url_for,
    request,
    session
)

import psycopg
from psycopg.rows import dict_row
from werkzeug.security import generate_password_hash, check_password_hash

import os
import re

# ============================================================
# ELITE FOREX ACADEMY
# MAIN APPLICATION
# ============================================================

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")

if not app.secret_key:
    app.secret_key = "temporary-local-development-key"


# ============================================================
# XM AFFILIATE SETTINGS
# ============================================================

XM_REFERRAL_LINK = os.environ.get(
    "XM_REFERRAL_LINK",
    "https://clicks.pipaffiliates.com/c?c=1347361&l=en&p=1"
)


# ============================================================
# NEON POSTGRESQL DATABASE
# ============================================================

DATABASE_URL = os.environ.get("DATABASE_URL")


def get_db():

    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL is not configured. "
            "Add your Neon PostgreSQL connection string."
        )

    connection = psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row
    )

    return connection


def initialize_database():

    connection = get_db()

    try:

        with connection.cursor() as cursor:

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS academy_members (

                    id BIGSERIAL PRIMARY KEY,

                    email TEXT UNIQUE NOT NULL,

                    password_hash TEXT NOT NULL,

                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

                )
            """)

        connection.commit()

    finally:

        connection.close()


# Initialize the database only when DATABASE_URL is configured.

if DATABASE_URL:
    initialize_database()

# ============================================================
# OFFICIAL BRAND COLOURS
# ============================================================

COLORS = {
    "navy": "#07111F",
    "black": "#05080D",
    "blue": "#00B8FF",
    "gold": "#D6AD60",
    "green": "#00D68F",
    "red": "#FF5263",
    "white": "#FFFFFF"
}

# ============================================================
# XM AFFILIATE SETTINGS
# ============================================================

XM_REFERRAL_LINK = os.environ.get(
    "XM_REFERRAL_LINK",
    "https://clicks.pipaffiliates.com/c?c=1347361&l=en&p=1"
)

# ============================================================
# NEON POSTGRESQL DATABASE INITIALIZATION
# ============================================================

DATABASE_URL = os.environ.get("DATABASE_URL")


def get_db():

    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not configured.")

    connection = psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row
    )

    return connection


def initialize_database():

    connection = get_db()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (

            id BIGSERIAL PRIMARY KEY,

            username TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    connection.commit()

    cursor.close()
    connection.close()


if DATABASE_URL:
    initialize_database()


# ============================================================
# WEBSITE DESIGN
# EVERYTHING IS GENERATED FROM PYTHON
# ============================================================

WEBSITE_TEMPLATE = """

<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Elite Forex Academy | Master the Markets</title>

<style>

:root {

    --navy: #07111F;
    --black: #05080D;
    --blue: #00B8FF;
    --gold: #D6AD60;
    --green: #00D68F;
    --red: #FF5263;
    --white: #FFFFFF;

}

* {

    margin: 0;
    padding: 0;
    box-sizing: border-box;

}

body {

    background: var(--navy);
    color: var(--white);

    font-family: Arial, sans-serif;

    overflow-x: hidden;

}

/* =====================================================
   NAVIGATION
===================================================== */

.navbar {

    width: 100%;

    height: 85px;

    display: flex;

    align-items: center;

    justify-content: space-between;

    padding: 0 7%;

    background: rgba(5,8,13,0.96);

    border-bottom: 1px solid rgba(214,173,96,0.18);

    position: sticky;

    top: 0;

    z-index: 1000;

}

.logo {

    font-size: 23px;

    font-weight: 900;

    letter-spacing: 2px;

    color: var(--gold);

}

.logo span {

    color: var(--white);

    display: block;

    font-size: 10px;

    letter-spacing: 5px;

    margin-top: 5px;

}

.nav-links {

    display: flex;

    align-items: center;

    gap: 30px;

}

.nav-links a {

    text-decoration: none;

    color: #C5CED9;

    font-size: 13px;

    transition: 0.3s;

}

.nav-links a:hover {

    color: var(--blue);

}

.nav-button {

    background: var(--blue);

    color: var(--black) !important;

    padding: 13px 20px;

    border-radius: 4px;

    font-weight: bold;

}

/* =====================================================
   HERO SECTION
===================================================== */

.hero {

    min-height: 650px;

    position: relative;
    overflow: hidden;

    display: flex;

    align-items: center;

    padding: 80px 9%;

    background:

    radial-gradient(
        circle at 80% 40%,
        rgba(0,184,255,0.12),
        transparent 35%
    ),

    linear-gradient(
        120deg,
        #07111F,
        #05080D
    );

}

.hero-content {

    max-width: 750px;

}

.hero-label {

    color: var(--gold);

    font-size: 12px;

    letter-spacing: 5px;

    margin-bottom: 25px;

}

.hero h1 {

    font-size: clamp(42px, 6vw, 75px);

    line-height: 1.08;

    font-weight: 900;

    margin-bottom: 25px;

}

.hero h1 span {

    color: var(--gold);

}

.hero-description {

    color: #AAB7C6;

    font-size: 16px;

    line-height: 1.9;

    max-width: 600px;

    margin-bottom: 35px;

}

.hero-buttons {

    display: flex;

    gap: 18px;

    flex-wrap: wrap;

}

.primary-button {

    background: var(--blue);

    color: var(--black);

    padding: 17px 28px;

    text-decoration: none;

    font-size: 13px;

    font-weight: bold;

    border-radius: 4px;

    transition: 0.3s;

}

.primary-button:hover {

    box-shadow: 0 0 25px rgba(0,184,255,0.4);

    transform: translateY(-3px);

}

.secondary-button {

    border: 1px solid var(--gold);

    color: var(--gold);

    padding: 17px 28px;

    text-decoration: none;

    font-size: 13px;

    font-weight: bold;

    border-radius: 4px;

}

/* =====================================================
   MARKET STATUS BAR
===================================================== */

.market-bar {

    display: flex;

    justify-content: space-around;

    flex-wrap: wrap;

    gap: 20px;

    padding: 25px 5%;

    background: var(--black);

    border-top: 1px solid #182536;

    border-bottom: 1px solid #182536;

}

.market-item {

    text-align: center;

}

.market-item small {

    color: #718096;

    font-size: 10px;

    letter-spacing: 2px;

}

.market-item h3 {

    margin-top: 8px;

    font-size: 18px;

}

.bullish {

    color: var(--green);

}

.bearish {

    color: var(--red);

}

/* =====================================================
   GENERAL SECTIONS
===================================================== */

.section {

    padding: 100px 8%;

}

.section-heading {

    text-align: center;

    margin-bottom: 55px;

}

.section-heading small {

    color: var(--gold);

    letter-spacing: 4px;

    font-size: 11px;

}

.section-heading h2 {

    font-size: 36px;

    margin-top: 15px;

}

.section-heading p {

    color: #8291A3;

    margin-top: 15px;

    line-height: 1.8;

}

/* =====================================================
   EDUCATION CARDS
===================================================== */

.education-grid {

    display: grid;

    grid-template-columns: repeat(3, 1fr);

    gap: 25px;

}

.education-card {

    background: var(--black);

    border: 1px solid #172638;

    padding: 35px;

    border-radius: 8px;

    transition: 0.3s;

}

.education-card:hover {

    border-color: var(--blue);

    transform: translateY(-7px);

}

.card-number {

    color: var(--gold);

    font-size: 13px;

    letter-spacing: 3px;

}

.education-card h3 {

    margin: 25px 0 15px;

    font-size: 22px;

}

.education-card p {

    color: #8997A8;

    line-height: 1.8;

    font-size: 14px;

}

.card-link {

    display: inline-block;

    color: var(--blue);

    text-decoration: none;

    margin-top: 25px;

    font-size: 13px;

}

/* =====================================================
   XM AFFILIATE SECTION
===================================================== */

.affiliate-section {

    background: linear-gradient(
        120deg,
        #05080D,
        #0C1B2C
    );

    text-align: center;

    padding: 100px 8%;

    border-top: 1px solid rgba(214,173,96,0.2);

    border-bottom: 1px solid rgba(214,173,96,0.2);

}

.affiliate-section h2 {

    font-size: 38px;

    margin-bottom: 20px;

}

.affiliate-section h2 span {

    color: var(--gold);

}

.affiliate-section p {

    color: #AAB7C6;

    max-width: 650px;

    margin: 0 auto 35px;

    line-height: 1.9;

}

/* =====================================================
   FOOTER
===================================================== */

footer {

    background: var(--black);

    padding: 55px 8% 25px;

    text-align: center;

}

footer .footer-logo {

    color: var(--gold);

    font-size: 23px;

    font-weight: bold;

    letter-spacing: 3px;

}

footer p {

    color: #718096;

    font-size: 12px;

    line-height: 2;

    margin-top: 20px;

}

.disclaimer {

    margin-top: 35px;

    border-top: 1px solid #1A2938;

    padding-top: 25px;

    color: #697789;

    font-size: 11px;

    line-height: 1.8;

}

/* =====================================================
   MOBILE RESPONSIVENESS
===================================================== */

@media(max-width: 900px) {

    .nav-links {

        gap: 12px;

    }

    .education-grid {

        grid-template-columns: repeat(2, 1fr);

    }

}

@media(max-width: 650px) {

    .navbar {

        height: auto;

        padding: 20px;

        align-items: flex-start;

        flex-direction: column;

        gap: 20px;

    }

    .nav-links {

        flex-wrap: wrap;

        gap: 15px;

    }

    .nav-links a {

        font-size: 11px;

    }

    .hero {

        padding: 80px 7%;

        min-height: 550px;

    }

    .education-grid {

        grid-template-columns: 1fr;

    }

    .section-heading h2 {

        font-size: 28px;

    }

    .affiliate-section h2 {

        font-size: 29px;

    }

}
/* ==========================================
   CONTINUOUS TRADING CHART ANIMATION
========================================== */

.hero-chart {

    position: absolute;

    inset: 0;

    width: 100%;

    height: 100%;

    opacity: 0.85;

    z-index: 0;

    pointer-events: none;

}

.hero::after {

    content: "";

    position: absolute;

    inset: 0;

    z-index: 1;

    background: linear-gradient(
        90deg,
        #07111F 5%,
        rgba(7,17,31,0.94) 35%,
        rgba(7,17,31,0.35) 100%
    );

    pointer-events: none;

}

.hero-content {

    position: relative;

    z-index: 2;

}

.trade-status {

    position: absolute;

    right: 7%;

    top: 35px;

    z-index: 3;

    color: #00B8FF;

    font-size: 11px;

    letter-spacing: 2px;

    background: rgba(5,8,13,0.8);

    border: 1px solid rgba(0,184,255,0.3);

    padding: 12px 18px;

    border-radius: 4px;

}

@media(max-width: 650px) {

    .hero-chart {

        opacity: 0.28;

    }

    .trade-status {

        top: 15px;

        right: 15px;

        font-size: 9px;

    }

}

</style>

</head>


<body>


<!-- NAVIGATION -->

<nav class="navbar">

    <div class="logo">

        ELITE

        <span>FOREX ACADEMY</span>

    </div>


    <div class="nav-links">

        <a href="/">HOME</a>

        <a href="/smc">SMC</a>

        <a href="/ict">ICT</a>

        <a href="/analysis">ANALYSIS</a>
        <a href="/strategies">Strategies</a>
        <a href="/platforms">Trading Apps</a>
        <a href="/about">ABOUT</a>

        <a href="/open-account" class="nav-button">

            CREATE ACCOUNT

        </a>
        <a href="/register" class="nav-button">
            JOIN ACADEMY
        </a>

        <a href="/login">
            MEMBER LOGIN
        </a>

    </div>

</nav>


<!-- PAGE CONTENT -->

{{ content | safe }}


<!-- FOOTER -->

<footer>

    <div class="footer-logo">

        ELITE FOREX ACADEMY

    </div>

    <p>

        MASTER THE MARKETS. TRADE WITH PRECISION.

        <br>

        Smart Money Concepts | ICT | Institutional Trading Education

    </p>


    <div class="disclaimer">

        Risk Warning: Forex and CFD trading involve significant risk

        and may not be suitable for all investors. You can lose your

        invested capital. Educational content is provided for

        informational purposes only and does not constitute

        financial advice.

        <br><br>

        Elite Forex Academy may receive compensation when visitors

        open trading accounts through our affiliate links.

    </div>

</footer>
<script>

/* ==========================================
   ELITE FOREX ACADEMY
   CONTINUOUS BUY AND SELL ANIMATION
========================================== */

(function() {

    const canvas = document.getElementById("tradingChart");

    if (!canvas) return;

    const ctx = canvas.getContext("2d");

    const status = document.getElementById("tradeStatus");

    const GREEN = "#00D68F";
    const RED = "#FF5263";
    const BLUE = "#00B8FF";
    const GOLD = "#D6AD60";

    let width = 0;
    let height = 0;

    // 10 seconds BUY, then 10 seconds SELL.
    const cycleDuration = 10000;

    const candleCount = 65;

    const reducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;


    function resize() {

        const rect = canvas.getBoundingClientRect();

        const ratio = Math.min(window.devicePixelRatio || 1, 2);

        width = rect.width;
        height = rect.height;

        canvas.width = width * ratio;
        canvas.height = height * ratio;

        ctx.setTransform(ratio, 0, 0, ratio, 0, 0);

    }


    function drawLine(y, color, label) {

        ctx.setLineDash([6, 5]);

        ctx.strokeStyle = color;
        ctx.lineWidth = 1.2;

        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();

        ctx.setLineDash([]);

        ctx.fillStyle = color;
        ctx.font = "bold 11px Arial";
        ctx.textAlign = "right";

        ctx.fillText(label, width - 12, y - 7);

    }


    function drawChart(time) {

        ctx.clearRect(0, 0, width, height);

        const direction =
            Math.floor(time / cycleDuration) % 2 === 0 ? 1 : -1;

        const phase =
            (time % cycleDuration) / cycleDuration;

        const color = direction === 1 ? GREEN : RED;

        const entry = height * 0.57;

        const movement = height * 0.27;

        const target = entry - direction * movement;

        const stop = entry + direction * movement * 0.5;


        // GRID

        ctx.strokeStyle = "rgba(120,150,180,0.12)";
        ctx.lineWidth = 1;

        for (let i = 0; i < 9; i++) {

            const y = height * i / 8;

            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(width, y);
            ctx.stroke();

        }

        for (let i = 0; i < 12; i++) {

            const x = width * i / 11;

            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, height);
            ctx.stroke();

        }


        // ENTRY, TP AND SL

        drawLine(entry, BLUE, "ENTRY");
        drawLine(target, GOLD, "TAKE PROFIT");
        drawLine(stop, RED, "STOP LOSS");


        // RISK REWARD INDICATOR

        ctx.fillStyle = "rgba(5,8,13,0.88)";
        ctx.fillRect(18, 18, 125, 58);

        ctx.strokeStyle = GOLD;
        ctx.strokeRect(18, 18, 125, 58);

        ctx.textAlign = "left";

        ctx.fillStyle = GOLD;
        ctx.font = "bold 11px Arial";
        ctx.fillText("RISK / REWARD", 28, 37);

        ctx.fillStyle = "#FFFFFF";
        ctx.font = "bold 18px Arial";
        ctx.fillText("1 : 2", 28, 61);


        // BUY OR SELL STATUS

        ctx.fillStyle = color;
        ctx.font = "bold 13px Arial";

        ctx.fillText(
            direction === 1 ? "BUY SETUP" : "SELL SETUP",
            18,
            105
        );


        // CANDLE ANIMATION

        const spacing = Math.max(5, (width - 35) / candleCount);

        const candleWidth = Math.max(
            5,
            Math.min(13, spacing * 0.85)
        );

        const progress = Math.min(1, phase * 1.2);

        for (let i = 0; i < candleCount; i++) {

            const x = 15 + i * spacing;

            const position = i / (candleCount - 1);

            if (position > progress) continue;

            const wave = Math.sin(i * 1.9) * height * 0.035;

            const noise = Math.sin(i * 3.7) * height * 0.018;

            const trend = direction * position * movement;

            const open = entry - trend + wave;

            const close =
                open - direction * height * 0.045 + noise;

            const high =
                Math.min(open, close) - height * 0.018;

            const low =
                Math.max(open, close) + height * 0.018;

            const candleColor = close < open ? GREEN : RED;


            // WICK

            ctx.strokeStyle = candleColor;
            ctx.lineWidth = 2;

            ctx.beginPath();
            ctx.moveTo(x, high);
            ctx.lineTo(x, low);
            ctx.stroke();


            // CANDLE BODY

            ctx.fillStyle = candleColor;

            ctx.fillRect(
                x - candleWidth / 2,
                Math.min(open, close),
                candleWidth,
                Math.max(3, Math.abs(close - open))
            );

        }


        // TAKE PROFIT HIT

        if (phase > 0.88) {

            ctx.fillStyle = GOLD;
            ctx.font = "bold 14px Arial";
            ctx.textAlign = "center";

            ctx.fillText(
                "TAKE PROFIT HIT ✓",
                width / 2,
                height - 25
            );

        }


        // TOP STATUS LABEL

        if (status) {

            status.style.color = color;

            status.innerHTML =
                "● SIMULATED " +
                (direction === 1 ? "BUY SETUP" : "SELL SETUP");

        }

    }


    function animate(timestamp) {

        if (!animate.startTime) {
            animate.startTime = timestamp;
        }

        const elapsed = timestamp - animate.startTime;

        drawChart(elapsed);

        if (!reducedMotion) {
            requestAnimationFrame(animate);
        }

    }


    resize();

    window.addEventListener("resize", resize);

    if (reducedMotion) {

        drawChart(0);

    } else {

        requestAnimationFrame(animate);

    }

})();

</script>


</body>

</html>

"""


# ============================================================
# PAGE RENDERING FUNCTION
# ============================================================

def render_page(content):

    return render_template_string(

        WEBSITE_TEMPLATE,

        content=content

    )
# ============================================================
# ELITE FOREX ACADEMY MEMBER ACCOUNTS
# ============================================================


# REGISTER

@app.route("/register", methods=["GET", "POST"])
def register():

    error = ""

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()

        password = request.form.get("password", "")

        confirm_password = request.form.get("confirm_password", "")

        if not email or not password:

            error = "Please complete all fields."

        elif not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):

            error = "Enter a valid email address."

        elif len(password) < 8:

            error = "Password must contain at least 8 characters."

        elif password != confirm_password:

            error = "Your passwords do not match."

        else:

            password_hash = generate_password_hash(password)

            try:

                with get_db() as connection:

                    with connection.cursor() as cursor:

                        cursor.execute("""
                            INSERT INTO academy_members
                            (email, password_hash)

                            VALUES (%s, %s)

                            RETURNING id
                        """, (email, password_hash))

                        member = cursor.fetchone()

                session.clear()

                session["member_id"] = member["id"]

                session["member_email"] = email

                return redirect(url_for("member_dashboard"))

            except psycopg.errors.UniqueViolation:

                error = "An account with this email already exists."

    content = f"""

    <section class="hero">

        <div class="hero-content">

            <div class="hero-label">JOIN ELITE FOREX ACADEMY</div>

            <h1>
                CREATE YOUR
                <span>MEMBER ACCOUNT.</span>
            </h1>

            <p class="hero-description">
                Create your account to access the academy.
            </p>

            <div style="
                max-width:450px;
                margin-top:30px;
            ">

                <form method="POST">

                    <input
                        type="email"
                        name="email"
                        placeholder="Email Address"
                        required
                        style="width:100%;padding:16px;margin-bottom:15px;"
                    >

                    <input
                        type="password"
                        name="password"
                        placeholder="Create Password"
                        minlength="8"
                        required
                        style="width:100%;padding:16px;margin-bottom:15px;"
                    >

                    <input
                        type="password"
                        name="confirm_password"
                        placeholder="Confirm Password"
                        minlength="8"
                        required
                        style="width:100%;padding:16px;margin-bottom:15px;"
                    >

                    <p style="color:#FF5263;margin-bottom:15px;">
                        {error}
                    </p>

                    <button
                        type="submit"
                        class="primary-button"
                        style="border:none;cursor:pointer;width:100%;"
                    >
                        CREATE ACCOUNT
                    </button>

                </form>

                <p style="margin-top:25px;">

                    Already registered?

                    <a href="/login" style="color:#00B8FF;">
                        LOGIN HERE
                    </a>

                </p>

            </div>

        </div>

    </section>

    """

    return render_page(content)


# ============================================================
# MEMBER LOGIN
# ============================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    error = ""

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()

        password = request.form.get("password", "")

        with get_db() as connection:

            with connection.cursor() as cursor:

                cursor.execute("""
                    SELECT id, email, password_hash

                    FROM academy_members

                    WHERE email = %s
                """, (email,))

                member = cursor.fetchone()

        if member and check_password_hash(
            member["password_hash"],
            password
        ):

            session.clear()

            session["member_id"] = member["id"]

            session["member_email"] = member["email"]

            return redirect(url_for("member_dashboard"))

        error = "Incorrect email or password."

    content = f"""

    <section class="hero">

        <div class="hero-content">

            <div class="hero-label">MEMBER ACCESS</div>

            <h1>
                WELCOME
                <span>BACK.</span>
            </h1>

            <p class="hero-description">
                Login to your Elite Forex Academy account.
            </p>

            <div style="max-width:450px;margin-top:30px;">

                <form method="POST">

                    <input
                        type="email"
                        name="email"
                        placeholder="Email Address"
                        required
                        style="width:100%;padding:16px;margin-bottom:15px;"
                    >

                    <input
                        type="password"
                        name="password"
                        placeholder="Password"
                        required
                        style="width:100%;padding:16px;margin-bottom:15px;"
                    >

                    <p style="color:#FF5263;margin-bottom:15px;">
                        {error}
                    </p>

                    <button
                        type="submit"
                        class="primary-button"
                        style="border:none;cursor:pointer;width:100%;"
                    >
                        LOGIN
                    </button>

                </form>

                <p style="margin-top:25px;">

                    Don't have an account?

                    <a href="/register" style="color:#00B8FF;">
                        REGISTER HERE
                    </a>

                </p>

            </div>

        </div>

    </section>

    """

    return render_page(content)


# ============================================================
# MEMBER DASHBOARD
# ============================================================

@app.route("/member-dashboard")
def member_dashboard():

    if "member_id" not in session:

        return redirect(url_for("login"))

    email = session.get("member_email", "")

    content = f"""

    <section class="hero">

        <div class="hero-content">

            <div class="hero-label">ELITE FOREX ACADEMY</div>

            <h1>
                MEMBER
                <span>DASHBOARD.</span>
            </h1>

            <p class="hero-description">
                Welcome to your academy account.
            </p>

            <div style="
                margin-top:35px;
                padding:30px;
                max-width:550px;
                background:rgba(5,8,13,0.85);
                border:1px solid rgba(0,184,255,0.35);
                border-radius:8px;
            ">

                <p style="color:#D6AD60;">
                    REGISTERED EMAIL
                </p>

                <h3 style="margin:15px 0;">
                    {email}
                </h3>

                <p style="color:#00D68F;">
                    ● ACCOUNT ACTIVE
                </p>

                <a href="/smc" class="primary-button"
                   style="display:inline-block;margin-top:25px;">
                    EXPLORE SMC LESSONS
                </a>

                <a href="/ict" class="secondary-button"
                   style="display:inline-block;margin-top:15px;">
                    EXPLORE ICT LESSONS
                </a>

                <br><br>

                <a href="/logout" style="color:#FF5263;">
                    LOG OUT
                </a>

            </div>

        </div>

    </section>

    """

    return render_page(content)


# ============================================================
# MEMBER LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ============================================================
# HOMEPAGE
# ============================================================

@app.route("/")

def home():

    content = """

    <section class="hero">
    <canvas
    id="tradingChart"
    class="hero-chart">
</canvas>

<div class="trade-status" id="tradeStatus">

    ● SIMULATED BUY SETUP

</div>

        <div class="hero-content">

            <div class="hero-label">

                THE NEXT LEVEL OF TRADING EDUCATION

            </div>


            <h1>

                MASTER THE MARKETS.

                <br>

                <span>TRADE WITH PRECISION.</span>

            </h1>


            <p class="hero-description">

                Discover the world of Smart Money Concepts and

                ICT trading methodologies. Understand market

                structure, liquidity, institutional price action

                and the principles behind professional market analysis.

            </p>


            <div class="hero-buttons">

                <a href="/smc" class="primary-button">

                    START LEARNING

                </a>


                <a href="/open-account" class="secondary-button">

                    CREATE TRADING ACCOUNT

                </a>

            </div>

        </div>

    </section>



    <section class="market-bar">

        <div class="market-item">

            <small>TRADING EDUCATION</small>

            <h3>SMC</h3>

        </div>


        <div class="market-item">

            <small>INSTITUTIONAL CONCEPTS</small>

            <h3>ICT</h3>

        </div>


        <div class="market-item">

            <small>MARKET STRUCTURE</small>

            <h3 class="bullish">PRICE ACTION</h3>

        </div>


        <div class="market-item">

            <small>LIQUIDITY ANALYSIS</small>

            <h3 class="bearish">SMART MONEY</h3>

        </div>

    </section>



    <section class="section">

        <div class="section-heading">

            <small>EXPLORE OUR ACADEMY</small>

            <h2>Master Institutional Trading</h2>

            <p>

                Build your understanding of how financial markets

                move through structured trading education.

            </p>

        </div>



        <div class="education-grid">


            <div class="education-card">

                <div class="card-number">01 / SMC</div>

                <h3>Smart Money Concepts</h3>

                <p>

                    Learn market structure, liquidity,

                    order blocks, fair value gaps,

                    inducement and institutional price action.

                </p>

                <a href="/smc" class="card-link">

                    EXPLORE SMC →

                </a>

            </div>



            <div class="education-card">

                <div class="card-number">02 / ICT</div>

                <h3>ICT Methodology</h3>

                <p>

                    Understand market structure shifts,

                    liquidity concepts, dealing ranges,

                    kill zones and ICT trading models.

                </p>

                <a href="/ict" class="card-link">

                    EXPLORE ICT →

                </a>

            </div>



            <div class="education-card">

                <div class="card-number">03 / ANALYSIS</div>

                <h3>Market Analysis</h3>

                <p>

                    Explore market direction, liquidity

                    positioning, technical structures

                    and educational chart breakdowns.

                </p>

                <a href="/analysis" class="card-link">

                    VIEW ANALYSIS →

                </a>

            </div>



        </div>

    </section>



    <section class="affiliate-section">

        <h2>

            START YOUR <span>TRADING JOURNEY</span>

        </h2>


        <p>

            Take the next step in your trading education.

            Explore the XM trading platform and learn about

            opening a trading account.

        </p>


        <a href="/open-account" class="primary-button">

            CREATE YOUR ACCOUNT

        </a>

    </section>

    """

    return render_page(content)

# ============================================================
# INTERACTIVE SMC EDUCATION PAGE
# ============================================================

@app.route("/smc")
def smc():

    content = """

    <style>

    .smc-library {
        display: grid;
        grid-template-columns: repeat(auto-fit,minmax(230px,1fr));
        gap: 18px;
        margin-top: 35px;
    }

    .smc-topic {
        background: #0B1522;
        border: 1px solid #263446;
        padding: 24px;
        border-radius: 9px;
        cursor: pointer;
        transition: 0.25s;
    }

    .smc-topic:hover {
        border-color: #00B8FF;
        transform: translateY(-4px);
        background: #101F30;
    }

    .smc-topic.active {
        border-color: #00B8FF;
        box-shadow: 0 0 18px rgba(0,184,255,0.15);
    }

    .smc-topic-number {
        color: #00B8FF;
        font-size: 11px;
        letter-spacing: 2px;
        margin-bottom: 14px;
    }

    .smc-topic h3 {
        color: white;
        margin-bottom: 12px;
    }

    .smc-topic p {
        color: #AAB7C6;
        font-size: 13px;
        line-height: 1.7;
    }

    .smc-topic-link {
        color: #00B8FF;
        font-size: 12px;
        margin-top: 18px;
        display: block;
    }

    .smc-learning-area {
        margin-top: 65px;
        scroll-margin-top: 100px;
    }

    .smc-lesson-header {
        margin-bottom: 30px;
    }

    .smc-lesson-header small {
        color: #00B8FF;
        letter-spacing: 2px;
    }

    .smc-lesson-header h2 {
        margin-top: 15px;
        font-size: 34px;
    }

    .smc-layout {
        display: grid;
        grid-template-columns: 1fr 1.5fr;
        gap: 25px;
        align-items: start;
    }

    .smc-box {
        background: #0B1522;
        border: 1px solid #263446;
        border-radius: 9px;
        padding: 25px;
        margin-bottom: 22px;
    }

    .smc-box h3 {
        color: white;
        margin-bottom: 16px;
    }

    .smc-box p {
        color: #AAB7C6;
        line-height: 1.85;
        font-size: 14px;
    }

    .smc-chart-container {
        background: #05080D;
        border: 1px solid #263446;
        border-radius: 9px;
        padding: 15px;
        overflow: hidden;
    }

    #smcChart {
        width: 100%;
        height: 340px;
        display: block;
    }

    .smc-chart-controls {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-bottom: 15px;
    }

    .smc-chart-controls button {
        background: #101F30;
        color: white;
        border: 1px solid #263446;
        padding: 10px 15px;
        cursor: pointer;
        border-radius: 4px;
    }

    .smc-chart-controls button.active {
        border-color: #00B8FF;
        color: #00B8FF;
    }

    .smc-note {
        border-left: 3px solid #D6AD60;
        background: rgba(214,173,96,0.07);
        padding: 17px;
        margin-top: 20px;
    }

    .smc-note p {
        color: #D6AD60;
    }

    .smc-navigation {
        display: flex;
        justify-content: space-between;
        gap: 15px;
        flex-wrap: wrap;
        margin-top: 30px;
    }

    .smc-navigation button {
        padding: 13px 22px;
        background: #101F30;
        color: white;
        border: 1px solid #263446;
        cursor: pointer;
        border-radius: 5px;
    }

    .smc-navigation button:hover {
        border-color: #00B8FF;
    }

    @media(max-width:800px) {

        .smc-layout {
            grid-template-columns: 1fr;
        }

        .smc-lesson-header h2 {
            font-size: 26px;
        }

        #smcChart {
            height: 280px;
        }

    }

    </style>


    <section class="hero">

        <div class="hero-content">

            <div class="hero-label">
                ELITE FOREX ACADEMY / SMART MONEY CONCEPTS
            </div>

            <h1>
                MASTER
                <span>SMART MONEY.</span>
            </h1>

            <p class="hero-description">

                Explore Smart Money Concepts through
                real candlestick examples, interactive
                charts and practical market explanations.

            </p>

            <div class="hero-buttons">

                <a href="#smc-library" class="primary-button">
                    EXPLORE CONCEPTS
                </a>

                <a href="#smc-learning" class="secondary-button">
                    OPEN LEARNING AREA
                </a>

            </div>

        </div>

    </section>


    <section class="section" id="smc-library">

        <div class="section-heading">

            <small>INTERACTIVE LEARNING LIBRARY</small>

            <h2>Explore SMC Concepts</h2>

            <p>
                Choose any concept you want to study.
                You do not need to follow a particular order.
            </p>

        </div>

        <div class="smc-library" id="smcTopicLibrary"></div>

    </section>


    <section class="section smc-learning-area" id="smc-learning">

        <div class="smc-lesson-header">

            <small id="smcLessonNumber">SELECT A CONCEPT</small>

            <h2 id="smcLessonTitle">
                Your Interactive Learning Area
            </h2>

            <p id="smcLessonSubtitle">
                Select any SMC concept above to begin.
            </p>

        </div>


        <div class="smc-chart-controls">

            <button id="smcBullishButton"
                    class="active"
                    onclick="changeSMCMode('bullish')">

                BULLISH EXAMPLE

            </button>

            <button id="smcBearishButton"
                    onclick="changeSMCMode('bearish')">

                BEARISH EXAMPLE

            </button>

        </div>


        <div class="smc-layout">

            <div>

                <div class="smc-box">

                    <h3>What Is This Concept?</h3>

                    <div id="smcExplanation"></div>

                </div>


                <div class="smc-box">

                    <h3>How To Identify It</h3>

                    <div id="smcIdentification"></div>

                </div>


                <div class="smc-box">

                    <h3>Trading Interpretation</h3>

                    <div id="smcInterpretation"></div>

                </div>


                <div class="smc-note">

                    <p id="smcWarning"></p>

                </div>

            </div>


            <div>

                <div class="smc-chart-container">

                    <h3 style="color:white;margin-bottom:15px;">
                        CANDLESTICK EXAMPLE
                    </h3>

                    <canvas id="smcChart"></canvas>

                    <p style="
                        color:#718096;
                        font-size:11px;
                        margin-top:12px;
                    ">

                        Educational candlestick illustration.
                        Green candles represent bullish movement.
                        Red candles represent bearish movement.

                    </p>

                </div>


                <div class="smc-box" style="margin-top:22px;">

                    <h3>What To Observe On The Chart</h3>

                    <div id="smcObservation"></div>

                </div>

            </div>

        </div>


        <div class="smc-navigation">

            <button onclick="goToSMCLibrary()">
                ← ALL CONCEPTS
            </button>

            <button onclick="openPreviousSMC()">
                PREVIOUS CONCEPT
            </button>

            <button onclick="openNextSMC()">
                NEXT CONCEPT →
            </button>

        </div>

    </section>


    <script>

    // ========================================================
    // SMC CONCEPT LIBRARY
    // Every concept can be opened independently.
    // ========================================================

    const smcLessons = [

    {
        title: "Market Structure",
        description: "Understand swing highs, swing lows and market direction.",

        explanation: `
        <p>
        Market structure describes how price forms
        significant highs and lows over time.
        </p>

        <p>
        A bullish structure generally forms Higher Highs
        and Higher Lows. A bearish structure generally
        forms Lower Highs and Lower Lows.
        </p>

        <p>
        A ranging market moves between relatively
        defined boundaries without a clear directional trend.
        </p>
        `,

        identification: `
        <p>Look for these formations:</p>
        <p>• HH - Higher High</p>
        <p>• HL - Higher Low</p>
        <p>• LH - Lower High</p>
        <p>• LL - Lower Low</p>
        <p>Identify significant swing points rather than
        treating every small candle movement as structure.</p>
        `,

        interpretation: `
        <p>
        Bullish structure suggests buyers are maintaining
        upward control.
        </p>
        <p>
        Bearish structure suggests sellers are maintaining
        downward control.
        </p>
        <p>
        A structural break against the existing trend
        may signal a change in market conditions.
        </p>
        `,

        observation: `
        <p>
        Observe how price creates successive swing points.
        </p>
        <p>
        Compare each new high and low with the previous
        significant high and low.
        </p>
        `,

        warning: "Do not classify every small candle high or low as a major structural swing."
    },


    {
        title: "Break of Structure (BOS)",
        description: "Learn how price breaks significant structural levels.",

        explanation: `
        <p>
        A Break of Structure occurs when price breaks
        an important previous swing level.
        </p>
        <p>
        In a bullish trend, a break above a significant
        swing high is commonly identified as bullish BOS.
        </p>
        <p>
        In a bearish trend, a break below a significant
        swing low is commonly identified as bearish BOS.
        </p>
        `,

        identification: `
        <p>1. Identify the existing market direction.</p>
        <p>2. Mark a significant swing high or low.</p>
        <p>3. Watch whether price breaks that level.</p>
        <p>4. Look for a candle close beyond the level
        as stronger confirmation.</p>
        `,

        interpretation: `
        <p>
        BOS is commonly used to identify continuation
        of an existing directional structure.
        </p>
        <p>
        A break should be evaluated in context, including
        the strength of the movement and the significance
        of the level.
        </p>
        `,

        observation: `
        <p>
        Watch the highlighted horizontal structural level.
        </p>
        <p>
        Notice how the candle closes beyond the previous
        swing point.
        </p>
        `,

        warning: "A wick passing a level does not always establish a confirmed structural break."
    },


    {
        title: "Change of Character (CHOCH)",
        description: "Understand the first potential signs of a directional change.",

        explanation: `
        <p>
        CHOCH means Change of Character.
        </p>
        <p>
        It describes a break against the existing
        directional structure that may indicate
        a developing market reversal.
        </p>
        <p>
        For example, in a bearish market, price breaking
        above a significant Lower High may suggest
        a possible bullish transition.
        </p>
        `,

        identification: `
        <p>1. Identify the existing trend.</p>
        <p>2. Mark the important protected swing point.</p>
        <p>3. Observe whether price breaks against
        the existing direction.</p>
        <p>4. Evaluate whether the break has convincing
        displacement and follow-through.</p>
        `,

        interpretation: `
        <p>
        A CHOCH can provide an early warning that
        the existing trend may be weakening.
        </p>
        <p>
        Traders often look for additional confirmation
        before considering a trade.
        </p>
        `,

        observation: `
        <p>
        Compare the previous trend with the candle
        that breaks the opposing structural level.
        </p>
        <p>
        Notice the possible change in directional momentum.
        </p>
        `,

        warning: "CHOCH is not a guarantee of reversal. False breaks can occur."
    },


    {
        title: "Liquidity",
        description: "Understand where stop orders and pending orders may accumulate.",

        explanation: `
        <p>
        In SMC trading, liquidity refers to areas where
        orders may be concentrated.
        </p>
        <p>
        Traders commonly study previous highs, previous
        lows, equal highs, equal lows and obvious
        support and resistance levels.
        </p>
        <p>
        These areas may attract price because of the
        orders placed around them.
        </p>
        `,

        identification: `
        <p>• Look for repeated highs.</p>
        <p>• Look for repeated lows.</p>
        <p>• Identify obvious swing points.</p>
        <p>• Mark areas where traders may place stop losses.</p>
        `,

        interpretation: `
        <p>
        Liquidity levels can help traders identify
        potential price targets and areas where
        a reaction may occur.
        </p>
        <p>
        A liquidity level is not automatically
        a reversal point.
        </p>
        `,

        observation: `
        <p>
        Observe the horizontal liquidity level.
        </p>
        <p>
        Notice how multiple candles approach
        the same price area.
        </p>
        `,

        warning: "Not every visible high or low contains the same amount of liquidity."
    },


    {
        title: "Buy-Side and Sell-Side Liquidity",
        description: "Learn BSL, SSL, equal highs and equal lows.",

        explanation: `
        <p>
        Buy-Side Liquidity (BSL) is commonly associated
        with buy stop orders above significant highs.
        </p>
        <p>
        Sell-Side Liquidity (SSL) is commonly associated
        with sell stop orders below significant lows.
        </p>
        <p>
        Equal highs and equal lows are common areas
        traders examine when mapping liquidity.
        </p>
        `,

        identification: `
        <p>BSL:</p>
        <p>• Mark significant swing highs.</p>
        <p>• Identify equal or closely aligned highs.</p>
        <br>
        <p>SSL:</p>
        <p>• Mark significant swing lows.</p>
        <p>• Identify equal or closely aligned lows.</p>
        `,

        interpretation: `
        <p>
        Traders may use BSL and SSL to identify
        possible liquidity targets.
        </p>
        <p>
        Price moving above a high or below a low
        may interact with orders around those levels.
        </p>
        `,

        observation: `
        <p>
        Study the repeated highs in the bullish example
        and repeated lows in the bearish example.
        </p>
        <p>
        The horizontal line represents the approximate
        liquidity area.
        </p>
        `,

        warning: "Equal highs and lows are approximate price areas, not necessarily identical prices."
    },


    {
        title: "Liquidity Sweeps",
        description: "Study price moving beyond a liquidity level and returning.",

        explanation: `
        <p>
        A liquidity sweep occurs when price moves
        beyond a level where liquidity is expected
        and then returns back across that level.
        </p>
        <p>
        A bullish example may involve price moving
        below a previous low before recovering.
        </p>
        <p>
        A bearish example may involve price moving
        above a previous high before falling back.
        </p>
        `,

        identification: `
        <p>1. Mark an important liquidity level.</p>
        <p>2. Wait for price to move beyond it.</p>
        <p>3. Observe whether price returns back inside.</p>
        <p>4. Look for additional confirmation.</p>
        `,

        interpretation: `
        <p>
        A sweep can provide context for a potential
        reversal or continuation setup.
        </p>
        <p>
        Traders may combine it with market structure,
        displacement and confirmation candles.
        </p>
        `,

        observation: `
        <p>
        Observe the candle wick passing the liquidity line.
        </p>
        <p>
        Notice that the candle closes back on the
        original side of the level.
        </p>
        `,

        warning: "A break beyond liquidity can become a genuine breakout rather than a sweep."
    },


    {
        title: "Inducement",
        description: "Understand potential liquidity traps before important price movements.",

        explanation: `
        <p>
        Inducement is an SMC concept describing a
        price level that may attract traders into
        taking positions before price moves toward
        another important liquidity area.
        </p>
        <p>
        Traders often examine minor swing highs,
        minor swing lows and obvious pullback points.
        </p>
        `,

        identification: `
        <p>1. Identify the broader market structure.</p>
        <p>2. Find an obvious minor swing point.</p>
        <p>3. Consider whether traders may be placing
        stops or entries around that level.</p>
        <p>4. Observe how price interacts with it.</p>
        `,

        interpretation: `
        <p>
        Inducement can help traders understand why
        price may move toward an obvious minor level
        before reaching a more significant area.
        </p>
        `,

        observation: `
        <p>
        Examine the smaller swing before the
        larger structural move.
        </p>
        <p>
        Study how price interacts with the minor level.
        </p>
        `,

        warning: "Inducement is interpretive. Do not label every minor swing as an intentional trap."
    },


    {
        title: "Order Blocks",
        description: "Study bullish and bearish order block formations.",

        explanation: `
        <p>
        An order block is commonly identified as
        a candle or price zone associated with
        a move that leads to significant displacement.
        </p>
        <p>
        A bullish order block is often identified
        around the last bearish candle before
        a strong upward move.
        </p>
        <p>
        A bearish order block is often identified
        around the last bullish candle before
        a strong downward move.
        </p>
        `,

        identification: `
        <p>1. Find a strong displacement move.</p>
        <p>2. Examine the candles immediately before it.</p>
        <p>3. Identify the relevant opposing candle.</p>
        <p>4. Mark the chosen candle range or body zone.</p>
        <p>5. Observe whether price later returns to the zone.</p>
        `,

        interpretation: `
        <p>
        Traders may watch an order block for a
        potential reaction when price revisits it.
        </p>
        <p>
        The quality of the zone depends on its context,
        displacement and surrounding market structure.
        </p>
        `,

        observation: `
        <p>
        Examine the highlighted candle before
        the strong directional movement.
        </p>
        <p>
        The shaded region represents an illustrative
        order block zone.
        </p>
        `,

        warning: "Not every opposite-coloured candle qualifies as a meaningful order block."
    },


    {
        title: "Fair Value Gaps (FVG)",
        description: "Understand three-candle imbalances and price inefficiencies.",

        explanation: `
        <p>
        A Fair Value Gap is commonly identified
        using a three-candle formation.
        </p>
        <p>
        A bullish FVG forms when the third candle's
        low is above the first candle's high.
        </p>
        <p>
        A bearish FVG forms when the third candle's
        high is below the first candle's low.
        </p>
        <p>
        The space between these prices is the
        imbalance zone.
        </p>
        `,

        identification: `
        <p>1. Identify three consecutive candles.</p>
        <p>2. Compare the first candle's high or low
        with the third candle's opposite extreme.</p>
        <p>3. Identify the gap between them.</p>
        <p>4. Mark the zone for observation.</p>
        `,

        interpretation: `
        <p>
        Traders often monitor FVGs because price
        may revisit an imbalance zone.
        </p>
        <p>
        A revisit does not guarantee a reaction
        or complete fill.
        </p>
        `,

        observation: `
        <p>
        Observe the three-candle formation.
        </p>
        <p>
        The shaded region represents the gap
        between the first and third candles.
        </p>
        `,

        warning: "A Fair Value Gap is not automatically a trading entry."
    },


    {
        title: "Displacement",
        description: "Recognize strong directional movement and momentum.",

        explanation: `
        <p>
        Displacement describes a strong directional
        price movement, often characterized by
        large candle bodies and limited overlap.
        </p>
        <p>
        In SMC analysis, displacement is often studied
        when price breaks important structure or
        creates an imbalance.
        </p>
        `,

        identification: `
        <p>• Look for relatively large candle bodies.</p>
        <p>• Observe consecutive directional candles.</p>
        <p>• Look for limited candle overlap.</p>
        <p>• Check whether important structure was broken.</p>
        `,

        interpretation: `
        <p>
        Strong displacement may suggest increasing
        directional momentum.
        </p>
        <p>
        Traders may then study the origin of the move
        and any imbalance left behind.
        </p>
        `,

        observation: `
        <p>
        Compare the large directional candles
        with the smaller candles preceding them.
        </p>
        <p>
        Notice the speed and distance of the movement.
        </p>
        `,

        warning: "A large candle alone does not establish a complete SMC setup."
    },


    {
        title: "Premium and Discount",
        description: "Understand the upper and lower halves of a dealing range.",

        explanation: `
        <p>
        Premium and Discount are used to describe
        price relative to a selected dealing range.
        </p>
        <p>
        The midpoint, commonly called equilibrium,
        divides the range into two halves.
        </p>
        <p>
        The upper half is premium.
        The lower half is discount.
        </p>
        `,

        identification: `
        <p>1. Select a meaningful swing high.</p>
        <p>2. Select a meaningful swing low.</p>
        <p>3. Measure the range between them.</p>
        <p>4. Mark the 50% midpoint.</p>
        `,

        interpretation: `
        <p>
        In a bullish context, traders often look
        for potential buying opportunities in discount.
        </p>
        <p>
        In a bearish context, traders often examine
        premium for potential selling opportunities.
        </p>
        `,

        observation: `
        <p>
        Observe the horizontal midpoint dividing
        the dealing range.
        </p>
        <p>
        The upper region is premium and the lower
        region is discount.
        </p>
        `,

        warning: "Premium and discount depend on the dealing range selected. The midpoint is not an automatic entry."
    },


    {
        title: "Mitigation",
        description: "Understand how price revisits previously formed zones.",

        explanation: `
        <p>
        Mitigation is commonly used to describe
        price returning to a previously identified
        trading zone.
        </p>
        <p>
        Traders may examine whether price revisits
        an order block or another important zone
        before continuing its movement.
        </p>
        `,

        identification: `
        <p>1. Identify a meaningful price zone.</p>
        <p>2. Observe the initial departure from it.</p>
        <p>3. Wait for price to return.</p>
        <p>4. Study the reaction inside or around the zone.</p>
        `,

        interpretation: `
        <p>
        A revisit may provide an opportunity to
        assess whether the original directional
        idea remains valid.
        </p>
        `,

        observation: `
        <p>
        Watch price move away from the highlighted
        zone and then return to it.
        </p>
        `,

        warning: "A revisit does not guarantee that a zone will hold."
    },


    {
        title: "Multi-Timeframe Analysis",
        description: "Combine higher and lower timeframe market information.",

        explanation: `
        <p>
        Multi-timeframe analysis involves studying
        price across different chart timeframes.
        </p>
        <p>
        A higher timeframe can provide broader
        directional context, while a lower timeframe
        can help examine detailed price action.
        </p>
        `,

        identification: `
        <p>1. Start with a higher timeframe.</p>
        <p>2. Identify the broader structure and direction.</p>
        <p>3. Move to an intermediate timeframe.</p>
        <p>4. Study liquidity and important zones.</p>
        <p>5. Use a lower timeframe to examine
        confirmation and possible entries.</p>
        `,

        interpretation: `
        <p>
        Traders use this approach to avoid studying
        an entry in isolation from the broader market.
        </p>
        <p>
        For example, a 15-minute chart may establish
        directional context, a 5-minute chart may
        show liquidity, and a 1-minute chart may
        provide entry confirmation.
        </p>
        `,

        observation: `
        <p>
        Compare the larger directional movement
        with the smaller price movements.
        </p>
        `,

        warning: "Different timeframes can show conflicting information. Always understand the timeframe hierarchy."
    },


    {
        title: "Complete SMC Trading Models",
        description: "Combine structure, liquidity, zones and confirmation.",

        explanation: `
        <p>
        An SMC trading model combines several
        concepts into a structured trading approach.
        </p>
        <p>
        A model may include market direction,
        liquidity interaction, displacement,
        an entry zone and confirmation.
        </p>
        `,

        identification: `
        <p>1. Establish directional context.</p>
        <p>2. Identify relevant liquidity.</p>
        <p>3. Wait for the required price reaction.</p>
        <p>4. Identify a meaningful entry zone.</p>
        <p>5. Define invalidation and potential targets.</p>
        `,

        interpretation: `
        <p>
        The purpose of combining concepts is to
        create a repeatable framework rather than
        entering because of one isolated signal.
        </p>
        `,

        observation: `
        <p>
        Observe how liquidity, a directional move,
        a retracement and confirmation can form
        parts of one trading model.
        </p>
        `,

        warning: "A complete trading model still carries risk. Always define position risk and invalidation."
    }

    ];


    // ========================================================
    // BUILD THE CONCEPT LIBRARY
    // ========================================================

    let currentSMC = 0;
    let smcMode = "bullish";

    const library = document.getElementById("smcTopicLibrary");

    smcLessons.forEach((lesson,index) => {

        const card = document.createElement("div");

        card.className = "smc-topic";

        card.innerHTML = `

            <div class="smc-topic-number">
                CONCEPT ${String(index + 1).padStart(2,"0")}
            </div>

            <h3>${lesson.title}</h3>

            <p>${lesson.description}</p>

            <span class="smc-topic-link">
                OPEN CONCEPT →
            </span>

        `;

        card.addEventListener("click", () => {
            openSMCLesson(index);
        });

        library.appendChild(card);

    });


    // ========================================================
    // OPEN ANY LESSON
    // ========================================================

    function openSMCLesson(index) {

        currentSMC = index;

        const lesson = smcLessons[index];

        document.getElementById("smcLessonNumber").textContent =
            "SMC CONCEPT " + String(index + 1).padStart(2,"0");

        document.getElementById("smcLessonTitle").textContent =
            lesson.title;

        document.getElementById("smcLessonSubtitle").textContent =
            lesson.description;

        document.getElementById("smcExplanation").innerHTML =
            lesson.explanation;

        document.getElementById("smcIdentification").innerHTML =
            lesson.identification;

        document.getElementById("smcInterpretation").innerHTML =
            lesson.interpretation;

        document.getElementById("smcObservation").innerHTML =
            lesson.observation;

        document.getElementById("smcWarning").textContent =
            lesson.warning;

        document.querySelectorAll(".smc-topic").forEach((card,i) => {
            card.classList.toggle("active",i === index);
        });

        drawSMCChart();

        document.getElementById("smc-learning").scrollIntoView({
            behavior:"smooth",
            block:"start"
        });

    }


    function changeSMCMode(mode) {

        smcMode = mode;

        document.getElementById("smcBullishButton")
            .classList.toggle("active",mode === "bullish");

        document.getElementById("smcBearishButton")
            .classList.toggle("active",mode === "bearish");

        drawSMCChart();

    }


    // ========================================================
    // CANDLESTICK CHART ENGINE
    // Draws actual OHLC candle bodies and wicks.
    // ========================================================

    function drawSMCChart() {

        const canvas = document.getElementById("smcChart");

        const rect = canvas.getBoundingClientRect();

        if (!rect.width) return;

        const ratio = window.devicePixelRatio || 1;

        canvas.width = rect.width * ratio;
        canvas.height = 340 * ratio;

        const ctx = canvas.getContext("2d");

        ctx.scale(ratio,ratio);

        const width = rect.width;
        const height = 340;

        ctx.fillStyle = "#05080D";
        ctx.fillRect(0,0,width,height);

        const bullish = smcMode === "bullish";

        const green = "#00D68F";
        const red = "#FF5263";
        const blue = "#00B8FF";
        const gold = "#D6AD60";

        const index = currentSMC;

        const labels = [
            "HH","BOS","CHOCH","BSL","BSL / SSL",
            "SWEEP","INDUCEMENT","ORDER BLOCK",
            "FVG","DISPLACEMENT","50% EQ","RETRACE","SMC MODEL"
        ];

        const label = labels[index];

        const count = 28;

        const left = 35;
        const right = width - 15;
        const top = 35;
        const bottom = height - 45;

        const chartHeight = bottom - top;

        const base = bullish ? 0.67 : 0.33;

        let prices = [];

        for(let i=0;i<count;i++) {

            let progress = i / (count - 1);

            let trend = bullish ? -progress * 0.34 : progress * 0.34;

            let wave = Math.sin(i * 0.85) * 0.055;

            let noise = Math.sin(i * 2.3) * 0.025;

            let special = 0;

            // Liquidity sweep
            if(index === 5 && i === 19) {
                special = bullish ? 0.17 : -0.17;
            }

            // CHOCH / BOS directional movement
            if((index === 1 || index === 2) && i > 18) {
                special = bullish ? -0.10 : 0.10;
            }

            // Displacement
            if(index === 9 && i > 18) {
                special = bullish ? -0.16 : 0.16;
            }

            // FVG movement
            if(index === 8 && i > 14 && i < 20) {
                special = bullish ? -0.12 : 0.12;
            }

            // Order block movement
            if(index === 7 && i > 20) {
                special = bullish ? 0.07 : -0.07;
            }

            prices.push(base + trend + wave + noise + special);

        }


        const spacing = (right-left) / count;

        const candleWidth = Math.max(4,spacing * 0.55);

        // Grid

        ctx.strokeStyle = "#182535";
        ctx.lineWidth = 1;

        for(let i=0;i<5;i++) {

            let y = top + i * chartHeight / 4;

            ctx.beginPath();
            ctx.moveTo(left,y);
            ctx.lineTo(right,y);
            ctx.stroke();

        }


        // Premium and discount background

        if(index === 10) {

            ctx.fillStyle = "rgba(255,82,99,0.10)";
            ctx.fillRect(left,top,right-left,chartHeight/2);

            ctx.fillStyle = "rgba(0,214,143,0.10)";
            ctx.fillRect(left,top+chartHeight/2,right-left,chartHeight/2);

            ctx.fillStyle = gold;
            ctx.font = "11px Arial";

            ctx.fillText("PREMIUM",left+5,top+18);
            ctx.fillText("DISCOUNT",left+5,bottom-8);

        }


        // Liquidity level

        if(index === 3 || index === 4 || index === 5 || index === 6) {

            let level = bullish ? top+chartHeight*0.30 : top+chartHeight*0.70;

            ctx.strokeStyle = gold;
            ctx.setLineDash([6,5]);

            ctx.beginPath();
            ctx.moveTo(left,level);
            ctx.lineTo(right,level);
            ctx.stroke();

            ctx.setLineDash([]);

            ctx.fillStyle = gold;
            ctx.font = "11px Arial";

            ctx.fillText("LIQUIDITY LEVEL",left+5,level-8);

        }


        // Order block zone

        if(index === 7 || index === 12) {

            let zoneY = top + chartHeight * 0.52;

            ctx.fillStyle = "rgba(0,184,255,0.15)";
            ctx.fillRect(left+spacing*15,zoneY,spacing*8,35);

            ctx.strokeStyle = blue;
            ctx.strokeRect(left+spacing*15,zoneY,spacing*8,35);

            ctx.fillStyle = blue;
            ctx.font = "11px Arial";
            ctx.fillText("ORDER BLOCK ZONE",left+spacing*15,zoneY-7);

        }


        // Fair value gap zone

        if(index === 8) {

            let gapY = top + chartHeight * 0.39;

            ctx.fillStyle = "rgba(0,184,255,0.20)";
            ctx.fillRect(left+spacing*13,gapY,spacing*6,35);

            ctx.strokeStyle = blue;
            ctx.strokeRect(left+spacing*13,gapY,spacing*6,35);

            ctx.fillStyle = blue;
            ctx.font = "11px Arial";
            ctx.fillText("FAIR VALUE GAP",left+spacing*13,gapY-7);

        }


        // Candles

        for(let i=0;i<count;i++) {

            let open = prices[i];

            let close = prices[i] + (Math.sin(i*1.8)*0.045);

            if(i > 19 && (index === 1 || index === 2 || index === 9)) {
                close += bullish ? -0.07 : 0.07;
            }

            let high = Math.min(open,close) - 0.025 - Math.abs(Math.sin(i))*0.018;

            let low = Math.max(open,close) + 0.025 + Math.abs(Math.cos(i))*0.018;

            // Create a sweep wick

            if(index === 5 && i === 19) {
                if(bullish) low += 0.19;
                else high -= 0.19;
            }

            let yOpen = top + open * chartHeight;
            let yClose = top + close * chartHeight;
            let yHigh = top + high * chartHeight;
            let yLow = top + low * chartHeight;

            let x = left + i * spacing + spacing/2;

            let candleColor = close < open ? green : red;

            ctx.strokeStyle = candleColor;
            ctx.fillStyle = candleColor;
            ctx.lineWidth = 1.5;

            // Wick

            ctx.beginPath();
            ctx.moveTo(x,yHigh);
            ctx.lineTo(x,yLow);
            ctx.stroke();

            // Body

            let bodyTop = Math.min(yOpen,yClose);
            let bodyHeight = Math.max(3,Math.abs(yClose-yOpen));

            ctx.fillRect(
                x-candleWidth/2,
                bodyTop,
                candleWidth,
                bodyHeight
            );

        }


        // Structural annotations

        ctx.fillStyle = blue;
        ctx.font = "bold 11px Arial";

        if(index === 0) {

            ctx.fillText("HH",left+spacing*23,top+30);
            ctx.fillText("HL",left+spacing*17,bottom-25);

        }

        if(index === 1 || index === 2) {

            ctx.fillText(label,left+spacing*20,top+25);

        }

        if(index === 5) {

            ctx.fillStyle = gold;
            ctx.fillText("SWEEP",left+spacing*18,top+chartHeight*0.80);

        }

        if(index === 8) {

            ctx.fillStyle = blue;
            ctx.fillText("3-CANDLE FVG",left+spacing*14,top+chartHeight*0.34);

        }

        if(index === 9) {

            ctx.fillStyle = gold;
            ctx.fillText("DISPLACEMENT",left+spacing*18,top+25);

        }


        // Chart heading

        ctx.fillStyle = "#AAB7C6";
        ctx.font = "11px Arial";

        ctx.fillText(
            bullish ? "BULLISH PRICE EXAMPLE" : "BEARISH PRICE EXAMPLE",
            left,
            18
        );

        ctx.fillText("PRICE",width-48,18);

        ctx.fillText("TIME →",width/2-20,height-12);

    }


    // ========================================================
    // NAVIGATION
    // ========================================================

    function goToSMCLibrary() {

        document.getElementById("smc-library").scrollIntoView({
            behavior:"smooth"
        });

    }


    function openNextSMC() {

        let next = (currentSMC + 1) % smcLessons.length;

        openSMCLesson(next);

    }


    function openPreviousSMC() {

        let previous =
            (currentSMC - 1 + smcLessons.length) % smcLessons.length;

        openSMCLesson(previous);

    }


    window.addEventListener("resize",function() {

        if(document.getElementById("smcLessonTitle").textContent !==
           "Your Interactive Learning Area") {
            drawSMCChart();
        }

    });


    </script>

    """

    return render_page(content)

# ============================================================
# INTERACTIVE ICT EDUCATION PAGE
# ============================================================

@app.route("/ict")
def ict():

    content = """

    <style>

    .ict-library {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
        gap: 18px;
        margin-top: 35px;
    }

    .ict-card {
        background: #0B1726;
        border: 1px solid rgba(0,184,255,0.15);
        padding: 25px;
        border-radius: 10px;
        cursor: pointer;
        transition: 0.3s;
    }

    .ict-card:hover {
        transform: translateY(-5px);
        border-color: #00B8FF;
        box-shadow: 0 10px 30px rgba(0,184,255,0.12);
    }

    .ict-card.active {
        border-color: #00B8FF;
        background: #102238;
    }

    .ict-number {
        color: #00B8FF;
        font-size: 12px;
        letter-spacing: 2px;
    }

    .ict-card h3 {
        color: white;
        margin: 12px 0;
        font-size: 18px;
    }

    .ict-card p {
        color: #9EADBD;
        font-size: 13px;
        line-height: 1.7;
    }

    .ict-lesson {
        display: none;
        margin-top: 55px;
        padding: 35px;
        background: #0B1726;
        border: 1px solid rgba(0,184,255,0.2);
        border-radius: 12px;
    }

    .ict-lesson.show {
        display: block;
    }

    .ict-lesson h2 {
        color: white;
        font-size: 30px;
        margin-bottom: 15px;
    }

    .ict-lesson p {
        color: #B4C1CE;
        line-height: 1.8;
    }

    .ict-definition {
        background: rgba(0,184,255,0.07);
        border-left: 3px solid #00B8FF;
        padding: 20px;
        margin: 25px 0;
        line-height: 1.8;
        color: #DCE8F3;
    }

    .ict-chart-box {
        background: #050B13;
        border: 1px solid rgba(0,184,255,0.18);
        padding: 15px;
        border-radius: 10px;
        margin-top: 25px;
    }

    .ict-chart-box canvas {
        width: 100%;
        height: 380px;
        display: block;
    }

    .ict-controls {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin: 20px 0;
    }

    .ict-controls button,
    .ict-navigation button {
        background: #102238;
        color: white;
        border: 1px solid rgba(0,184,255,0.35);
        padding: 12px 20px;
        border-radius: 5px;
        cursor: pointer;
    }

    .ict-controls button:hover,
    .ict-navigation button:hover {
        background: #00B8FF;
        color: #05080D;
    }

    .ict-navigation {
        display: flex;
        justify-content: space-between;
        gap: 15px;
        margin-top: 30px;
    }

    .ict-explanation {
        margin-top: 30px;
        padding: 25px;
        background: rgba(255,255,255,0.025);
        border-radius: 8px;
    }

    .ict-explanation h3 {
        color: #00B8FF;
        margin-bottom: 12px;
    }

    .ict-explanation ul {
        padding-left: 20px;
        color: #B4C1CE;
        line-height: 2;
    }

    .ict-disclaimer {
        color: #8293A5;
        font-size: 12px;
        margin-top: 15px;
    }

    @media(max-width:650px) {

        .ict-lesson {
            padding: 20px;
        }

        .ict-chart-box canvas {
            height: 280px;
        }

        .ict-lesson h2 {
            font-size: 24px;
        }

    }

    </style>


    <section class="hero">

        <div class="hero-content">

            <div class="hero-label">
                ELITE EDUCATION / ICT METHODOLOGY
            </div>

            <h1>
                INNER CIRCLE
                <span>TRADER.</span>
            </h1>

            <p class="hero-description">

                Explore the ICT methodology through interactive
                candlestick examples, institutional concepts,
                liquidity delivery and precision trading models.

            </p>

        </div>

    </section>


    <section class="section">

        <div class="section-heading">

            <small>ICT CONCEPT LIBRARY</small>

            <h2>Explore Institutional Trading</h2>

            <p style="color:#9EADBD;max-width:750px;margin:auto;">

                Choose any concept below to study it.
                You do not need to follow a particular order.
                Each lesson includes an illustrative bullish
                and bearish market example.

            </p>

        </div>


        <div class="ict-library" id="ictLibrary"></div>


        <div class="ict-lesson" id="ictLesson">

            <div class="ict-number" id="ictLessonNumber"></div>

            <h2 id="ictLessonTitle"></h2>

            <p id="ictLessonIntro"></p>


            <div class="ict-definition">

                <strong>CORE CONCEPT</strong>

                <p id="ictDefinition"></p>

            </div>


            <h3 style="color:white;margin-top:30px;">

                Interactive Candlestick Example

            </h3>


            <p>

                Switch between bullish and bearish examples
                to explore how this concept can appear in price.

            </p>


            <div class="ict-controls">

                <button onclick="drawICTChart('BULLISH')">

                    BULLISH EXAMPLE

                </button>

                <button onclick="drawICTChart('BEARISH')">

                    BEARISH EXAMPLE

                </button>

            </div>


            <div class="ict-chart-box">

                <canvas id="ictChart"></canvas>

            </div>

            <p class="ict-disclaimer">

                Educational illustration only. Candles are
                simulated examples, not live or historical market data.

            </p>


            <div class="ict-explanation">

                <h3>How To Identify It</h3>

                <ul id="ictIdentification"></ul>

            </div>


            <div class="ict-explanation">

                <h3>How Traders Interpret It</h3>

                <p id="ictInterpretation"></p>

            </div>


            <div class="ict-explanation">

                <h3>Common Mistakes</h3>

                <ul id="ictMistakes"></ul>

            </div>


            <div class="ict-navigation">

                <button onclick="previousICT()">

                    ← PREVIOUS CONCEPT

                </button>

                <button onclick="nextICT()">

                    NEXT CONCEPT →

                </button>

            </div>

        </div>

    </section>


    <script>

    const ictConcepts = [

        {
            title: "ICT Market Structure",
            intro: "Understand how price forms directional movements through swing highs and swing lows.",
            definition: "ICT market structure examines the sequence of significant highs and lows to understand whether price is moving bullishly, bearishly or transitioning.",
            identification: [
                "Identify significant swing highs and swing lows.",
                "Look for higher highs and higher lows in bullish conditions.",
                "Look for lower highs and lower lows in bearish conditions.",
                "Observe whether price breaks an important structural level."
            ],
            interpretation: "Market structure provides directional context. Traders use it alongside liquidity, displacement and other ICT concepts rather than relying on one swing alone.",
            mistakes: [
                "Treating every small candle movement as a structural change.",
                "Ignoring the timeframe being analysed.",
                "Assuming structure alone provides an entry."
            ]
        },

        {
            title: "Market Structure Shift (MSS)",
            intro: "Study how a displacement move can signal a potential change in short-term order flow.",
            definition: "A Market Structure Shift occurs when price breaks a relevant opposing swing point, often following a liquidity raid and a strong displacement move.",
            identification: [
                "Identify the prevailing short-term direction.",
                "Observe a possible liquidity raid.",
                "Look for displacement in the opposite direction.",
                "Confirm that price breaks a relevant swing point."
            ],
            interpretation: "An MSS can suggest that short-term order flow is changing. Traders may then study a retracement into an FVG or another relevant PD array.",
            mistakes: [
                "Calling every small swing break an MSS.",
                "Ignoring displacement.",
                "Entering before the structural break is confirmed."
            ]
        },

        {
            title: "Liquidity Pools",
            intro: "Understand why areas containing clusters of stop orders attract price.",
            definition: "Liquidity pools are areas where orders may accumulate, particularly around obvious highs, lows and repeated price levels.",
            identification: [
                "Mark obvious swing highs and swing lows.",
                "Look for repeated highs or repeated lows.",
                "Identify previous session highs and lows.",
                "Observe how price approaches these areas."
            ],
            interpretation: "Traders monitor liquidity pools as potential price objectives or areas where a reaction may occur. The presence of a level does not guarantee a reversal.",
            mistakes: [
                "Assuming every liquidity level must be taken.",
                "Ignoring higher-timeframe context.",
                "Treating an estimated liquidity area as confirmed order flow."
            ]
        },

        {
            title: "Buy-Side and Sell-Side Liquidity",
            intro: "Learn the difference between liquidity resting above highs and below lows.",
            definition: "Buy-side liquidity (BSL) is commonly associated with buy stops above highs. Sell-side liquidity (SSL) is commonly associated with sell stops below lows.",
            identification: [
                "Mark significant swing highs for potential BSL.",
                "Mark significant swing lows for potential SSL.",
                "Look for equal highs and equal lows.",
                "Include previous day and session extremes."
            ],
            interpretation: "Price may seek liquidity above highs or below lows before continuing or reversing. Traders use these levels to frame potential market objectives.",
            mistakes: [
                "Confusing BSL with ordinary buying pressure.",
                "Confusing SSL with ordinary selling pressure.",
                "Assuming a liquidity target guarantees a reversal."
            ]
        },

        {
            title: "Liquidity Sweeps",
            intro: "Understand what happens when price trades beyond a liquidity level and then rejects it.",
            definition: "A liquidity sweep occurs when price moves through a known liquidity area, such as a previous high or low, and then fails to sustain that breakout.",
            identification: [
                "Identify an obvious liquidity level.",
                "Observe price trading beyond the level.",
                "Look for rejection or a close back through the level.",
                "Seek additional confirmation before considering an entry."
            ],
            interpretation: "A sweep can provide context for a possible reversal, especially when followed by displacement and a market structure shift.",
            mistakes: [
                "Calling every breakout a sweep.",
                "Entering immediately without confirmation.",
                "Ignoring strong continuation beyond the level."
            ]
        },

        {
            title: "Fair Value Gap (FVG)",
            intro: "Study price imbalances created by strong directional movement.",
            definition: "A Fair Value Gap is a three-candle price imbalance. A bullish FVG forms when the first candle's high is below the third candle's low. A bearish FVG forms when the first candle's low is above the third candle's high.",
            identification: [
                "Identify three consecutive candles.",
                "For bullish FVG: compare candle one's high with candle three's low.",
                "For bearish FVG: compare candle one's low with candle three's high.",
                "Mark the imbalance between the non-overlapping wicks."
            ],
            interpretation: "Traders may monitor an FVG as a potential retracement area. Its significance depends on context, displacement and surrounding price structure.",
            mistakes: [
                "Marking a gap without checking all three candles.",
                "Assuming every FVG will be filled.",
                "Ignoring the direction and quality of displacement."
            ]
        },

        {
            title: "Inversion Fair Value Gap (IFVG)",
            intro: "Explore how a previously respected FVG can become a level that acts in the opposite direction.",
            definition: "An Inversion Fair Value Gap occurs when price violates an existing fair value gap and subsequently uses that area as potential support or resistance from the opposite side.",
            identification: [
                "Identify a valid bullish or bearish FVG.",
                "Observe price moving through the gap.",
                "Watch for a close beyond the relevant boundary.",
                "Monitor a return to the gap from the opposite side."
            ],
            interpretation: "An IFVG can provide a potential reaction area after a shift in price behaviour. Traders commonly combine it with liquidity and structure.",
            mistakes: [
                "Calling every FVG touch an inversion.",
                "Ignoring whether price actually violated the gap.",
                "Entering without observing the return reaction."
            ]
        },

        {
            title: "Order Blocks",
            intro: "Understand the candle area associated with a significant displacement move.",
            definition: "An ICT order block is commonly identified as the last opposing candle before a meaningful displacement that breaks structure or drives price away from the area.",
            identification: [
                "Identify a meaningful displacement move.",
                "Locate the last opposing candle before that move.",
                "Check whether the move breaks relevant structure.",
                "Mark the candle range as a potential reaction area."
            ],
            interpretation: "Traders may monitor a return to an order block for a potential reaction. Not every opposing candle qualifies as a meaningful order block.",
            mistakes: [
                "Marking every last bearish or bullish candle.",
                "Ignoring displacement and structural context.",
                "Assuming every order block must hold."
            ]
        },

        {
            title: "Breaker Blocks",
            intro: "Study failed order blocks that may become potential support or resistance from the opposite side.",
            definition: "A breaker block is generally associated with a failed order block. Price breaks through the original area, and the area may later act as support or resistance in the opposite direction.",
            identification: [
                "Identify a meaningful original order block.",
                "Observe price breaking through that block.",
                "Look for a return to the broken area.",
                "Study the reaction from the opposite side."
            ],
            interpretation: "A breaker may provide a potential entry area when aligned with liquidity and directional context.",
            mistakes: [
                "Calling every broken candle an ICT breaker.",
                "Ignoring the original order block.",
                "Assuming the retest will always hold."
            ]
        },

        {
            title: "Mitigation Blocks",
            intro: "Explore price returning to an area associated with previous institutional order flow.",
            definition: "A mitigation block is an ICT price-action concept associated with a failed swing or price delivery sequence, where price revisits an area before continuing or changing direction.",
            identification: [
                "Study the preceding market structure.",
                "Identify the relevant swing and displacement.",
                "Mark the potential mitigation area.",
                "Observe how price reacts on its return."
            ],
            interpretation: "Traders use mitigation blocks as contextual price areas, often alongside liquidity and market structure.",
            mistakes: [
                "Confusing mitigation blocks with ordinary order blocks.",
                "Ignoring the preceding price sequence.",
                "Treating every retracement as mitigation."
            ]
        },

        {
            title: "Optimal Trade Entry (OTE)",
            intro: "Learn how Fibonacci retracement levels are used to identify potential entry areas.",
            definition: "ICT Optimal Trade Entry uses a Fibonacci retracement of a defined price swing. The commonly referenced OTE zone is approximately 62% to 79%, with 70.5% often highlighted.",
            identification: [
                "Identify a clear directional price swing.",
                "For a bullish retracement, measure from swing low to swing high.",
                "For a bearish retracement, measure from swing high to swing low.",
                "Monitor the 62% to 79% retracement area."
            ],
            interpretation: "OTE is a potential retracement framework, not an automatic entry signal. Traders may seek confluence with an FVG, order block or liquidity event.",
            mistakes: [
                "Drawing Fibonacci across unrelated swings.",
                "Entering solely because price reaches 70.5%.",
                "Ignoring the prevailing directional context."
            ]
        },

        {
            title: "Premium and Discount",
            intro: "Understand how price is evaluated relative to the midpoint of a defined dealing range.",
            definition: "The dealing range is divided using its equilibrium (50%) level. Price above equilibrium is premium, while price below equilibrium is discount.",
            identification: [
                "Identify a meaningful dealing range.",
                "Mark the range high and range low.",
                "Calculate the 50% equilibrium.",
                "Identify whether price is in premium or discount."
            ],
            interpretation: "In a bullish context, traders often prefer studying discount areas. In a bearish context, they often study premium areas. This is a framework, not a guarantee.",
            mistakes: [
                "Using an arbitrary range.",
                "Ignoring the timeframe.",
                "Assuming premium automatically means sell or discount automatically means buy."
            ]
        },

        {
            title: "Judas Swing",
            intro: "Study a false directional move that may occur around a trading session's opening period.",
            definition: "The Judas Swing describes a move that initially runs in one direction, potentially taking liquidity, before price moves in the opposite direction.",
            identification: [
                "Understand the session context.",
                "Mark nearby liquidity levels.",
                "Observe an initial move into liquidity.",
                "Look for rejection and displacement in the opposite direction."
            ],
            interpretation: "The concept is used to frame potential session reversals. The initial move alone does not confirm a Judas Swing.",
            mistakes: [
                "Assuming every opening move is a Judas Swing.",
                "Ignoring session timing.",
                "Entering before opposite-direction confirmation."
            ]
        },

        {
            title: "Power of Three (PO3)",
            intro: "Understand the accumulation, manipulation and distribution framework.",
            definition: "Power of Three describes a price-delivery model involving accumulation, manipulation and distribution. Price may consolidate, move against the intended direction and then expand.",
            identification: [
                "Identify a consolidation or accumulation range.",
                "Observe a possible manipulation beyond the range.",
                "Look for displacement away from the range.",
                "Study the resulting directional expansion."
            ],
            interpretation: "PO3 provides a framework for understanding possible price delivery during a session or larger trading period.",
            mistakes: [
                "Forcing every chart into the PO3 pattern.",
                "Confusing ordinary volatility with manipulation.",
                "Assuming distribution must occur."
            ]
        },

        {
            title: "Kill Zones",
            intro: "Learn how ICT identifies important periods of trading activity.",
            definition: "ICT Kill Zones refer to specific time windows associated with increased trading activity around major market sessions, particularly London and New York.",
            identification: [
                "Understand the London session window.",
                "Understand the New York session window.",
                "Use the appropriate time zone and daylight-saving adjustment.",
                "Observe liquidity and price delivery during the window."
            ],
            interpretation: "Kill Zones help traders focus their analysis during selected periods. They do not guarantee volatility or profitable setups.",
            mistakes: [
                "Using incorrect time-zone conversions.",
                "Assuming every Kill Zone produces a setup.",
                "Ignoring major economic news."
            ]
        },

        {
            title: "Daily Bias",
            intro: "Develop a directional framework for analysing the trading day.",
            definition: "Daily bias is a directional expectation based on higher-timeframe structure, liquidity objectives, price delivery and relevant market context.",
            identification: [
                "Review higher-timeframe market structure.",
                "Mark previous day high and low.",
                "Identify nearby liquidity objectives.",
                "Study price behaviour around important levels."
            ],
            interpretation: "Daily bias helps organise intraday analysis. It should be updated when market conditions invalidate the original expectation.",
            mistakes: [
                "Deciding bias from one candle.",
                "Refusing to update a bias after invalidation.",
                "Confusing a directional expectation with certainty."
            ]
        },

        {
            title: "SMT Divergence",
            intro: "Explore relative price differences between correlated markets.",
            definition: "SMT divergence is a comparison between correlated instruments where one makes a new high or low while the other fails to do so.",
            identification: [
                "Choose two markets with a meaningful relationship.",
                "Compare corresponding swing highs or lows.",
                "Observe whether one market takes liquidity while the other does not.",
                "Look for confirmation from structure and price delivery."
            ],
            interpretation: "SMT divergence can provide additional context about relative market strength or weakness. Correlation is not constant.",
            mistakes: [
                "Comparing unrelated instruments.",
                "Using mismatched timeframes.",
                "Treating divergence as a standalone entry signal."
            ]
        },

        {
            title: "ICT Trading Models",
            intro: "Bring liquidity, structure, displacement and PD arrays together into a repeatable trading framework.",
            definition: "ICT trading models combine multiple concepts into a structured sequence for analysing market direction, identifying liquidity objectives and locating potential entries.",
            identification: [
                "Establish higher-timeframe directional context.",
                "Identify a relevant liquidity objective.",
                "Observe a sweep or another meaningful price event.",
                "Look for displacement and market structure confirmation.",
                "Study a retracement into a relevant PD array."
            ],
            interpretation: "A trading model helps create consistent rules for setup selection, entry, invalidation and risk management. No model guarantees a winning trade.",
            mistakes: [
                "Taking setups without the required conditions.",
                "Changing rules from trade to trade.",
                "Ignoring stop-loss placement and risk management."
            ]
        }

    ];


    let currentICT = 0;
    let ictDirection = "BULLISH";


    const ictLibrary = document.getElementById("ictLibrary");


    ictConcepts.forEach((concept, index) => {

        const card = document.createElement("div");

        card.className = "ict-card";

        card.innerHTML = `

            <div class="ict-number">

                CONCEPT ${String(index + 1).padStart(2, "0")}

            </div>

            <h3>${concept.title}</h3>

            <p>${concept.intro}</p>

        `;

        card.onclick = () => openICT(index);

        ictLibrary.appendChild(card);

    });


    function openICT(index) {

        currentICT = (index + ictConcepts.length) % ictConcepts.length;

        const concept = ictConcepts[currentICT];

        document.getElementById("ictLesson").classList.add("show");

        document.getElementById("ictLessonNumber").textContent =
            "ICT CONCEPT " + (currentICT + 1) + " / " + ictConcepts.length;

        document.getElementById("ictLessonTitle").textContent =
            concept.title;

        document.getElementById("ictLessonIntro").textContent =
            concept.intro;

        document.getElementById("ictDefinition").textContent =
            concept.definition;

        document.getElementById("ictInterpretation").textContent =
            concept.interpretation;


        const identification = document.getElementById("ictIdentification");

        identification.innerHTML = "";

        concept.identification.forEach(item => {

            const li = document.createElement("li");

            li.textContent = item;

            identification.appendChild(li);

        });


        const mistakes = document.getElementById("ictMistakes");

        mistakes.innerHTML = "";

        concept.mistakes.forEach(item => {

            const li = document.createElement("li");

            li.textContent = item;

            mistakes.appendChild(li);

        });


        document.querySelectorAll(".ict-card").forEach((card, i) => {

            card.classList.toggle("active", i === currentICT);

        });


        drawICTChart(ictDirection);

        document.getElementById("ictLesson").scrollIntoView({

            behavior: "smooth",

            block: "start"

        });

    }


    function previousICT() {

        openICT(currentICT - 1);

    }


    function nextICT() {

        openICT(currentICT + 1);

    }


    function drawICTChart(direction) {

        ictDirection = direction;

        const canvas = document.getElementById("ictChart");

        const ctx = canvas.getContext("2d");

        const rect = canvas.getBoundingClientRect();

        const width = rect.width;

        const height = rect.height;

        const dpr = window.devicePixelRatio || 1;

        canvas.width = width * dpr;

        canvas.height = height * dpr;

        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);


        ctx.clearRect(0, 0, width, height);

        ctx.fillStyle = "#050B13";

        ctx.fillRect(0, 0, width, height);


        const candles = 55;

        const spacing = width / (candles + 2);

        const candleWidth = Math.max(3, spacing * 0.55);

        let prices = [];

        let base = height * 0.55;

        const movement = direction === "BULLISH" ? -1 : 1;


        for (let i = 0; i < candles; i++) {

            let trend = movement * i * 0.85;

            let wave = Math.sin(i * 0.7) * 14;

            let noise = Math.sin(i * 2.3) * 5;

            let close = base + trend + wave + noise;

            prices.push(close);

        }


        const minPrice = Math.min(...prices) - 35;

        const maxPrice = Math.max(...prices) + 35;

        const range = maxPrice - minPrice || 1;


        function y(price) {

            return 25 + ((price - minPrice) / range) * (height - 50);

        }


        // CHART GRID

        ctx.strokeStyle = "rgba(255,255,255,0.06)";

        ctx.lineWidth = 1;

        for (let i = 0; i < 6; i++) {

            const gy = 30 + i * (height - 60) / 5;

            ctx.beginPath();

            ctx.moveTo(0, gy);

            ctx.lineTo(width, gy);

            ctx.stroke();

        }


        // CANDLESTICKS

        for (let i = 0; i < candles; i++) {

            const x = (i + 1) * spacing;

            const close = prices[i];

            const open = i === 0 ? close + 5 : prices[i - 1];

            const volatility = 8 + Math.abs(Math.sin(i * 1.7)) * 10;

            const high = Math.min(open, close) - volatility;

            const low = Math.max(open, close) + volatility;

            const bullish = close < open;

            const candleColor = bullish ? "#00D68F" : "#FF5263";


            ctx.strokeStyle = candleColor;

            ctx.lineWidth = 1.5;

            ctx.beginPath();

            ctx.moveTo(x, y(high));

            ctx.lineTo(x, y(low));

            ctx.stroke();


            ctx.fillStyle = candleColor;

            const top = Math.min(y(open), y(close));

            const bottom = Math.max(y(open), y(close));

            ctx.fillRect(

                x - candleWidth / 2,

                top,

                candleWidth,

                Math.max(2, bottom - top)

            );

        }


        // CHART ANNOTATIONS

        const concept = ictConcepts[currentICT];

        const title = concept.title.toUpperCase();

        ctx.font = "bold 11px Arial";

        ctx.fillStyle = "#00B8FF";

        ctx.fillText(title, 15, 20);


        // Highlight an illustrative price area.

        const zoneX = width * 0.48;

        const zoneY = height * 0.43;

        const zoneWidth = width * 0.27;

        const zoneHeight = 35;


        ctx.fillStyle = "rgba(0,184,255,0.10)";

        ctx.fillRect(zoneX, zoneY, zoneWidth, zoneHeight);

        ctx.strokeStyle = "rgba(0,184,255,0.65)";

        ctx.strokeRect(zoneX, zoneY, zoneWidth, zoneHeight);


        ctx.fillStyle = "#00B8FF";

        ctx.font = "10px Arial";

        ctx.fillText("ILLUSTRATIVE AREA", zoneX + 5, zoneY - 7);


        // Direction label

        ctx.fillStyle = direction === "BULLISH" ? "#00D68F" : "#FF5263";

        ctx.font = "bold 12px Arial";

        ctx.fillText(direction + " EXAMPLE", 15, height - 12);

    }


    window.addEventListener("resize", function() {

        if (document.getElementById("ictLesson").classList.contains("show")) {

            drawICTChart(ictDirection);

        }

    });


    // Open the first concept automatically.

    openICT(0);


    </script>

    """

    return render_page(content)

# ============================================================
# INTERACTIVE MARKET ANALYSIS PAGE
# ============================================================

@app.route("/analysis")
def analysis():

    content = """

    <style>

    .market-intro {
        max-width: 800px;
        margin: auto;
        text-align: center;
    }

    .market-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin-top: 40px;
    }

    .market-card {
        background: #0B1726;
        border: 1px solid rgba(0,184,255,0.15);
        border-radius: 10px;
        padding: 28px;
        cursor: pointer;
        transition: 0.3s;
    }

    .market-card:hover {
        transform: translateY(-5px);
        border-color: #00B8FF;
        box-shadow: 0 10px 30px rgba(0,184,255,0.10);
    }

    .market-card.active {
        border-color: #00B8FF;
        background: #102238;
    }

    .market-card small {
        color: #00B8FF;
        letter-spacing: 2px;
        font-size: 11px;
    }

    .market-card h3 {
        color: white;
        margin: 15px 0;
        font-size: 23px;
    }

    .market-card p {
        color: #9EADBD;
        line-height: 1.7;
        font-size: 13px;
    }

    .market-panel {
        display: none;
        margin-top: 45px;
        background: #0B1726;
        border: 1px solid rgba(0,184,255,0.2);
        border-radius: 12px;
        padding: 35px;
    }

    .market-panel.show {
        display: block;
    }

    .market-panel h2 {
        color: white;
        font-size: 29px;
        margin-bottom: 15px;
    }

    .market-panel h3 {
        color: #00B8FF;
        margin-bottom: 15px;
    }

    .market-panel p {
        color: #AAB8C7;
        line-height: 1.8;
    }

    .market-watchlist {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 12px;
        margin: 25px 0;
    }

    .watch-item {
        background: #07111F;
        padding: 18px;
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 7px;
    }

    .watch-item strong {
        color: white;
        display: block;
        margin-bottom: 8px;
    }

    .watch-item span {
        color: #8293A5;
        font-size: 11px;
    }

    .market-info-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
        gap: 18px;
        margin-top: 30px;
    }

    .market-info {
        background: #07111F;
        padding: 22px;
        border-radius: 8px;
        border: 1px solid rgba(255,255,255,0.06);
    }

    .market-info h4 {
        color: white;
        margin-bottom: 12px;
    }

    .market-info p {
        font-size: 13px;
    }

    .analysis-workflow {
        margin-top: 65px;
    }

    .analysis-step {
        display: flex;
        gap: 20px;
        padding: 22px;
        background: #0B1726;
        border: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 12px;
        border-radius: 8px;
    }

    .step-number {
        color: #00B8FF;
        font-size: 23px;
        font-weight: bold;
    }

    .analysis-step h4 {
        color: white;
        margin-bottom: 8px;
    }

    .analysis-step p {
        color: #9EADBD;
        font-size: 13px;
        line-height: 1.7;
    }

    .analysis-disclaimer {
        padding: 20px;
        border-left: 3px solid #D6AD60;
        background: rgba(214,173,96,0.06);
        margin-top: 35px;
        color: #AAB8C7;
        font-size: 13px;
        line-height: 1.8;
    }

    @media(max-width:650px) {

        .market-panel {
            padding: 20px;
        }

        .market-panel h2 {
            font-size: 23px;
        }

        .analysis-step {
            padding: 15px;
        }

    }

    </style>


    <section class="hero">

        <div class="hero-content">

            <div class="hero-label">
                ELITE MARKET INTELLIGENCE
            </div>

            <h1>

                UNDERSTAND

                <span>PRICE ACTION.</span>

            </h1>

            <p class="hero-description">

                Explore forex, gold and cryptocurrency markets
                through institutional concepts, technical analysis
                and professional trading methodologies.

            </p>

        </div>

    </section>


    <section class="section">

        <div class="section-heading">

            <small>MARKET INTELLIGENCE</small>

            <h2>Explore The Markets</h2>

            <p style="color:#9EADBD;max-width:750px;margin:auto;">

                Select a market to explore its analysis framework,
                important instruments and institutional trading concepts.

            </p>

        </div>


        <div class="market-grid">

            <div class="market-card" onclick="openMarket('forex',this)">

                <small>01 / CURRENCY MARKETS</small>

                <h3>Forex Markets</h3>

                <p>

                    Explore major and minor currency pairs,
                    currency strength, market structure and
                    institutional price delivery.

                </p>

                <span style="color:#00B8FF;font-size:12px;">

                    EXPLORE FOREX →

                </span>

            </div>


            <div class="market-card" onclick="openMarket('gold',this)">

                <small>02 / PRECIOUS METALS</small>

                <h3>Gold Analysis</h3>

                <p>

                    Study XAUUSD price action, liquidity,
                    volatility, market structure and
                    institutional trading opportunities.

                </p>

                <span style="color:#00B8FF;font-size:12px;">

                    EXPLORE GOLD →

                </span>

            </div>


            <div class="market-card" onclick="openMarket('crypto',this)">

                <small>03 / DIGITAL ASSETS</small>

                <h3>Crypto Markets</h3>

                <p>

                    Explore Bitcoin, Ethereum and other
                    cryptocurrency markets through technical
                    and institutional analysis.

                </p>

                <span style="color:#00B8FF;font-size:12px;">

                    EXPLORE CRYPTO →

                </span>

            </div>

        </div>


        <div class="market-panel" id="marketPanel">

            <small id="marketCategory" style="color:#00B8FF;"></small>

            <h2 id="marketTitle"></h2>

            <p id="marketDescription"></p>


            <h3 style="margin-top:35px;">

                Instruments To Follow

            </h3>

            <div class="market-watchlist" id="marketWatchlist"></div>


            <div class="market-info-grid">

                <div class="market-info">

                    <h4>Market Structure</h4>

                    <p id="marketStructure"></p>

                </div>


                <div class="market-info">

                    <h4>Liquidity Analysis</h4>

                    <p id="marketLiquidity"></p>

                </div>


                <div class="market-info">

                    <h4>Institutional Concepts</h4>

                    <p id="marketInstitutional"></p>

                </div>


                <div class="market-info">

                    <h4>Risk Management</h4>

                    <p id="marketRisk"></p>

                </div>

            </div>

        </div>


        <div class="analysis-workflow">

            <div class="section-heading">

                <small>PROFESSIONAL ANALYSIS FRAMEWORK</small>

                <h2>How We Analyse The Markets</h2>

                <p style="color:#9EADBD;">

                    A structured approach to understanding
                    price movement and potential trading opportunities.

                </p>

            </div>


            <div class="analysis-step">

                <div class="step-number">01</div>

                <div>

                    <h4>Higher Timeframe Direction</h4>

                    <p>

                        Study the higher timeframe to understand
                        the prevailing market direction, important
                        swing points and potential price objectives.

                    </p>

                </div>

            </div>


            <div class="analysis-step">

                <div class="step-number">02</div>

                <div>

                    <h4>Liquidity Identification</h4>

                    <p>

                        Identify buy-side liquidity, sell-side
                        liquidity, equal highs, equal lows and
                        important previous session levels.

                    </p>

                </div>

            </div>


            <div class="analysis-step">

                <div class="step-number">03</div>

                <div>

                    <h4>Market Structure Confirmation</h4>

                    <p>

                        Study displacement, Break of Structure,
                        Change of Character and Market Structure Shift
                        to understand potential changes in price direction.

                    </p>

                </div>

            </div>


            <div class="analysis-step">

                <div class="step-number">04</div>

                <div>

                    <h4>Entry Area Identification</h4>

                    <p>

                        Examine Fair Value Gaps, Order Blocks,
                        Breaker Blocks and other relevant price
                        delivery areas.

                    </p>

                </div>

            </div>


            <div class="analysis-step">

                <div class="step-number">05</div>

                <div>

                    <h4>Trade Planning</h4>

                    <p>

                        Define the potential entry, invalidation
                        level, Stop Loss, Take Profit and
                        Risk-to-Reward before considering a trade.

                    </p>

                </div>

            </div>


            <div class="analysis-step">

                <div class="step-number">06</div>

                <div>

                    <h4>Fundamental Context</h4>

                    <p>

                        Consider economic announcements, interest
                        rate decisions, inflation data and other
                        events that may influence market volatility.

                    </p>

                </div>

            </div>

        </div>


        <div class="analysis-disclaimer">

            <strong>MARKET RISK NOTICE</strong><br><br>

            Market analysis is educational and does not constitute
            financial advice or a guarantee of future results.
            Financial markets involve substantial risk.
            Always conduct your own research and apply appropriate
            risk management.

        </div>


    </section>


    <script>

    const marketData = {

        forex: {

            category: "CURRENCY MARKETS",

            title: "Forex Market Analysis",

            description:
                "Analyse currency pairs by examining relative currency strength, economic conditions, market structure and liquidity. Focus on how one currency performs against another.",

            instruments: [
                ["EURUSD", "Euro / US Dollar"],
                ["GBPUSD", "British Pound / US Dollar"],
                ["USDJPY", "US Dollar / Japanese Yen"],
                ["GBPJPY", "British Pound / Japanese Yen"],
                ["EURJPY", "Euro / Japanese Yen"],
                ["USDCAD", "US Dollar / Canadian Dollar"],
                ["AUDUSD", "Australian Dollar / US Dollar"],
                ["USDCHF", "US Dollar / Swiss Franc"]
            ],

            structure:
                "Examine higher highs, higher lows, lower highs, lower lows, BOS and CHOCH across multiple timeframes.",

            liquidity:
                "Monitor previous day highs and lows, session highs and lows, equal highs, equal lows and important swing liquidity.",

            institutional:
                "Study liquidity sweeps, displacement, Fair Value Gaps, Order Blocks, Premium and Discount.",

            risk:
                "Account for spread, volatility, position size and the distance between entry and invalidation."
        },


        gold: {

            category: "PRECIOUS METALS",

            title: "Gold Market Analysis",

            description:
                "Explore XAUUSD through market structure, liquidity, macroeconomic context and institutional price delivery. Gold can experience significant volatility during major economic announcements.",

            instruments: [
                ["XAUUSD", "Gold / US Dollar"],
                ["DXY", "US Dollar Index"],
                ["EURUSD", "Euro / US Dollar"],
                ["USDJPY", "US Dollar / Japanese Yen"]
            ],

            structure:
                "Study major gold swings, higher timeframe direction, displacement and important structural breaks.",

            liquidity:
                "Monitor previous day high and low, Asian session range, London session levels and New York session liquidity.",

            institutional:
                "Examine liquidity raids, MSS, FVG, Order Blocks, OTE and premium or discount positioning.",

            risk:
                "Gold can move rapidly. Consider spread, slippage, volatility and appropriately sized positions."
        },


        crypto: {

            category: "DIGITAL ASSETS",

            title: "Cryptocurrency Market Analysis",

            description:
                "Study digital assets through price action, market structure, liquidity and broader cryptocurrency market conditions. Cryptocurrency markets operate around the clock.",

            instruments: [
                ["BTCUSD", "Bitcoin / US Dollar"],
                ["ETHUSD", "Ethereum / US Dollar"],
                ["BTCGBP", "Bitcoin / British Pound"],
                ["BTCJPY", "Bitcoin / Japanese Yen"]
            ],

            structure:
                "Identify major swing highs and lows, directional movement, structural breaks and consolidation ranges.",

            liquidity:
                "Monitor equal highs, equal lows, previous swing points and important consolidation boundaries.",

            institutional:
                "Study displacement, FVG, liquidity sweeps, Order Blocks and market structure shifts.",

            risk:
                "Cryptocurrency prices can be highly volatile. Consider exchange conditions, leverage and position sizing."
        }

    };


    function openMarket(type, card) {

        const data = marketData[type];

        if (!data) return;


        document.querySelectorAll(".market-card").forEach(item => {

            item.classList.remove("active");

        });

        card.classList.add("active");


        document.getElementById("marketCategory").textContent =
            data.category;

        document.getElementById("marketTitle").textContent =
            data.title;

        document.getElementById("marketDescription").textContent =
            data.description;


        const watchlist = document.getElementById("marketWatchlist");

        watchlist.innerHTML = "";


        data.instruments.forEach(instrument => {

            const item = document.createElement("div");

            item.className = "watch-item";

            const name = document.createElement("strong");

            name.textContent = instrument[0];

            const description = document.createElement("span");

            description.textContent = instrument[1];

            item.appendChild(name);

            item.appendChild(description);

            watchlist.appendChild(item);

        });


        document.getElementById("marketStructure").textContent =
            data.structure;

        document.getElementById("marketLiquidity").textContent =
            data.liquidity;

        document.getElementById("marketInstitutional").textContent =
            data.institutional;

        document.getElementById("marketRisk").textContent =
            data.risk;


        const panel = document.getElementById("marketPanel");

        panel.classList.add("show");

        panel.scrollIntoView({

            behavior: "smooth",

            block: "start"

        });

    }

    </script>

    """

    return render_page(content)
# ============================================================
# INTERACTIVE STRATEGIES PAGE
# ============================================================

@app.route("/strategies")
def strategies():

    content = """

    <style>

        .strategy-hero {
            padding: 100px 9%;
            background: linear-gradient(120deg, #07111F, #05080D);
        }

        .strategy-label {
            color: #D6AD60;
            letter-spacing: 3px;
            font-size: 12px;
            font-weight: bold;
            margin-bottom: 20px;
        }

        .strategy-hero h1 {
            font-size: clamp(40px, 6vw, 72px);
            line-height: 1.1;
            margin-bottom: 25px;
        }

        .strategy-hero h1 span {
            color: #00B8FF;
        }

        .strategy-hero p {
            max-width: 650px;
            color: #AAB7C5;
            line-height: 1.8;
        }

        .strategy-section {
            padding: 75px 9%;
        }

        .strategy-heading {
            margin-bottom: 35px;
        }

        .strategy-heading h2 {
            font-size: 30px;
            margin-bottom: 12px;
        }

        .strategy-heading p {
            color: #9AA9B8;
        }

        .strategy-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 22px;
        }

        .strategy-card {
            background: #0B1726;
            border: 1px solid rgba(0,184,255,0.15);
            border-radius: 12px;
            padding: 28px;
            cursor: pointer;
            transition: 0.3s;
        }

        .strategy-card:hover {
            transform: translateY(-6px);
            border-color: #00B8FF;
            box-shadow: 0 10px 35px rgba(0,184,255,0.12);
        }

        .strategy-number {
            color: #D6AD60;
            font-size: 13px;
            letter-spacing: 2px;
            margin-bottom: 20px;
        }

        .strategy-card h3 {
            font-size: 21px;
            margin-bottom: 14px;
        }

        .strategy-card p {
            color: #9AA9B8;
            line-height: 1.7;
            font-size: 14px;
        }

        .strategy-open {
            display: inline-block;
            margin-top: 22px;
            color: #00B8FF;
            font-size: 13px;
            font-weight: bold;
        }

        .strategy-detail {
            display: none;
            margin-top: 45px;
            padding: 35px;
            background: #0B1726;
            border: 1px solid rgba(0,184,255,0.25);
            border-radius: 14px;
        }

        .strategy-detail.active {
            display: block;
        }

        .strategy-detail h2 {
            font-size: 30px;
            margin-bottom: 15px;
        }

        .strategy-detail > p {
            color: #AAB7C5;
            line-height: 1.8;
        }

        .strategy-columns {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }

        .strategy-info {
            background: #07111F;
            border-radius: 9px;
            padding: 22px;
            border: 1px solid rgba(255,255,255,0.06);
        }

        .strategy-info h3 {
            color: #00B8FF;
            margin-bottom: 15px;
            font-size: 17px;
        }

        .strategy-info p,
        .strategy-info li {
            color: #AAB7C5;
            font-size: 14px;
            line-height: 1.8;
        }

        .strategy-info ul {
            padding-left: 18px;
        }

        .bullish-text {
            color: #00D68F !important;
        }

        .bearish-text {
            color: #FF5263 !important;
        }

        .strategy-warning {
            margin-top: 25px;
            padding: 20px;
            border-left: 3px solid #D6AD60;
            background: rgba(214,173,96,0.07);
            color: #C4CDD6;
            line-height: 1.7;
            font-size: 14px;
        }

        .strategy-close {
            margin-top: 25px;
            background: transparent;
            border: 1px solid #00B8FF;
            color: #00B8FF;
            padding: 11px 22px;
            border-radius: 5px;
            cursor: pointer;
        }
        .strategy-chart-wrap {
    margin-top: 35px;
    background: #050B13;
    border: 1px solid rgba(0,184,255,0.25);
    border-radius: 12px;
    padding: 20px;
    overflow: hidden;
}

.strategy-chart-heading {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 15px;
    margin-bottom: 15px;
    flex-wrap: wrap;
}

.strategy-chart-heading h3 {
    color: #FFFFFF;
    font-size: 17px;
}

.strategy-status {
    color: #00D68F;
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 1px;
}

.strategy-chart {
    width: 100%;
    height: 360px;
    display: block;
}

.strategy-chart-note {
    color: #8293A5;
    font-size: 12px;
    margin-top: 12px;
}

@media(max-width: 600px) {
    .strategy-chart {
        height: 280px;
    }
}

        @media(max-width: 600px) {

            .strategy-hero,
            .strategy-section {
                padding: 65px 6%;
            }

            .strategy-detail {
                padding: 22px;
            }

        }

    </style>


    <section class="strategy-hero">

        <div class="strategy-label">
            ELITE FOREX ACADEMY / TRADING MODELS
        </div>

        <h1>
            MASTER YOUR
            <span>ENTRY.</span>
        </h1>

        <p>
            Explore institutional-style trading strategies
            built around liquidity, market structure,
            displacement and price confirmation.

            Understand the conditions behind each setup
            before considering a trade.
        </p>

    </section>


    <section class="strategy-section">

        <div class="strategy-heading">

            <h2>Trading Strategy Library</h2>

            <p>
                Select a strategy to explore its setup,
                entry conditions and trade management.
            </p>

        </div>


        <div class="strategy-grid">

            <div class="strategy-card"
                 onclick="openStrategy('liquidity')">

                <div class="strategy-number">MODEL 01</div>

                <h3>Liquidity Sweep Model</h3>

                <p>
                    Identify liquidity resting above highs
                    or below lows, then study the reaction
                    after price takes those levels.
                </p>

                <span class="strategy-open">
                    EXPLORE STRATEGY →
                </span>

            </div>


            <div class="strategy-card"
                 onclick="openStrategy('orderblock')">

                <div class="strategy-number">MODEL 02</div>

                <h3>Order Block Model</h3>

                <p>
                    Study institutional order block zones,
                    displacement and potential price
                    reactions on a return to the zone.
                </p>

                <span class="strategy-open">
                    EXPLORE STRATEGY →
                </span>

            </div>


            <div class="strategy-card"
                 onclick="openStrategy('mss')">

                <div class="strategy-number">MODEL 03</div>

                <h3>MSS Entry Model</h3>

                <p>
                    Combine a liquidity event with a
                    market structure shift and a
                    retracement into a defined entry area.
                </p>

                <span class="strategy-open">
                    EXPLORE STRATEGY →
                </span>

            </div>


            <div class="strategy-card"
                 onclick="openStrategy('fvg')">

                <div class="strategy-number">MODEL 04</div>

                <h3>FVG Retracement Model</h3>

                <p>
                    Study fair value gaps created by
                    displacement and how price may
                    react when returning to the imbalance.
                </p>

                <span class="strategy-open">
                    EXPLORE STRATEGY →
                </span>

            </div>

        </div>


        <!-- STRATEGY DETAILS -->

        <div class="strategy-detail" id="strategyDetail">

            <div id="strategyContent"></div>

            <button class="strategy-close"
                    onclick="closeStrategy()">

                CLOSE STRATEGY

            </button>

        </div>

    </section>


    <script>

    const strategiesData = {

        liquidity: {

            title: "Liquidity Sweep Model",

            description:
            "This model studies how price interacts with important liquidity levels. A sweep occurs when price trades beyond a previous high or low and then reacts back across that level. A sweep alone does not guarantee a reversal.",

            direction: "Bullish and Bearish",

            timeframe: "Higher timeframe for context; lower timeframe for confirmation.",

            entry: [
                "Identify a meaningful previous swing high or swing low.",
                "Wait for price to trade beyond that liquidity level.",
                "Look for price to close back inside the level.",
                "Wait for lower-timeframe confirmation.",
                "Plan an entry only when the setup provides a defined risk."
            ],

            bullish:
            "Price moves below a previous swing low, takes sell-side liquidity and then closes back above the level. Look for bullish confirmation before considering a long position.",

            bearish:
            "Price moves above a previous swing high, takes buy-side liquidity and then closes back below the level. Look for bearish confirmation before considering a short position.",

            stop:
            "A logical invalidation level is beyond the sweep extreme, with an appropriate buffer for volatility.",

            target:
            "Potential targets include opposing liquidity, previous swing levels or other valid reaction areas.",

            warning:
            "Not every liquidity sweep produces a reversal. Strong trends can continue after taking liquidity. Always consider the higher-timeframe context."
        },


        orderblock: {

            title: "Order Block Model",

            description:
            "An order block is commonly studied as the last opposing candle or candle range before a significant displacement move that contributes to a market structure break. The zone is then monitored for a possible return and reaction.",

            direction: "Bullish and Bearish",

            timeframe: "Higher timeframe for context; lower timeframe for entry confirmation.",

            entry: [
                "Identify a meaningful market structure level.",
                "Find the opposing candle or candle range before displacement.",
                "Confirm that the displacement is significant and supports a structure break.",
                "Mark the order block boundaries.",
                "Wait for price to return to the zone and assess confirmation."
            ],

            bullish:
            "A bullish order block is generally identified around the final bearish candle or range before strong bullish displacement. A return to the zone may offer a potential long setup.",

            bearish:
            "A bearish order block is generally identified around the final bullish candle or range before strong bearish displacement. A return to the zone may offer a potential short setup.",

            stop:
            "The invalidation level is generally placed beyond the order block boundary, adjusted for volatility and the specific setup.",

            target:
            "Consider opposing liquidity, previous highs or lows, and other valid market reaction levels.",

            warning:
            "Not every opposing candle is an order block. Context, displacement and market structure matter. A revisit does not guarantee a reaction."
        },


        mss: {

            title: "MSS Entry Model",

            description:
            "A Market Structure Shift (MSS) is a change in short-term price structure that may indicate a change in directional pressure. This model combines a liquidity event, a structure shift and a retracement into a defined entry zone.",

            direction: "Bullish and Bearish",

            timeframe: "Higher timeframe for directional bias; lower timeframe for the setup and confirmation.",

            entry: [
                "Establish the higher-timeframe directional context.",
                "Identify a meaningful liquidity level.",
                "Wait for price to sweep that liquidity.",
                "Look for displacement and a break of relevant short-term structure.",
                "Define the flip-and-sweep range that produced the shift.",
                "Wait for price to retrace into the defined range.",
                "Look for confirmation before considering entry."
            ],

            bullish:
            "After sell-side liquidity is swept, price produces bullish displacement and breaks relevant short-term structure. The resulting flip-and-sweep area is monitored for a retracement and bullish confirmation.",

            bearish:
            "After buy-side liquidity is swept, price produces bearish displacement and breaks relevant short-term structure. The resulting flip-and-sweep area is monitored for a retracement and bearish confirmation.",

            stop:
            "Place the invalidation level beyond the relevant setup extreme or zone boundary, with a suitable buffer.",

            target:
            "Use valid opposing liquidity or other clearly identified reaction areas to plan the target and evaluate risk-to-reward.",

            warning:
            "A market structure shift without a meaningful setup context can produce false signals. Do not treat every minor structure break as a valid MSS."
        },


        fvg: {

            title: "FVG Retracement Model",

            description:
            "A Fair Value Gap is a three-candle price imbalance commonly identified when the first and third candles do not overlap across a price range. Traders study these areas as potential retracement zones.",

            direction: "Bullish and Bearish",

            timeframe: "Higher timeframe for context; lower timeframe for entry confirmation.",

            entry: [
                "Identify a strong displacement move.",
                "Locate the three-candle imbalance.",
                "Mark the boundaries of the Fair Value Gap.",
                "Evaluate whether the gap aligns with market structure and directional context.",
                "Wait for price to return to the gap.",
                "Look for confirmation before considering an entry."
            ],

            bullish:
            "A bullish FVG forms during upward displacement when the first candle's high is below the third candle's low. Price may later retrace into the gap before continuing upward.",

            bearish:
            "A bearish FVG forms during downward displacement when the first candle's low is above the third candle's high. Price may later retrace into the gap before continuing downward.",

            stop:
            "Define invalidation using the relevant setup structure or FVG boundaries, depending on the trading plan.",

            target:
            "Potential targets include opposing liquidity, previous swing points or other valid reaction zones.",

            warning:
            "An FVG is not automatically a trading signal. Consider displacement quality, market structure, liquidity and the wider market context."
        }

    };


    function openStrategy(type) {

        const data = strategiesData[type];

        if (!data) return;

        const steps = data.entry.map((step, index) => {

            return `
                <li>${step}</li>
            `;

        }).join("");


        document.getElementById("strategyContent").innerHTML = `

            <div class="strategy-label">
                ELITE TRADING MODEL
            </div>

            <h2>${data.title}</h2>

            <p>${data.description}</p>
            <div class="strategy-chart-wrap">

    <div class="strategy-chart-heading">

        <h3>LIVE STRATEGY SIMULATION</h3>

        <span class="strategy-status" id="strategyStatus">
            ANALYSING MARKET...
        </span>

    </div>

    <canvas
        id="strategyChart"
        class="strategy-chart">
    </canvas>

    <div class="strategy-chart-note">
        Illustrative animated price action. Not live market data.
    </div>

</div>


            <div class="strategy-columns">

                <div class="strategy-info">

                    <h3>SETUP CONDITIONS</h3>

                    <ul>${steps}</ul>

                </div>


                <div class="strategy-info">

                    <h3>TIMEFRAME APPROACH</h3>

                    <p>${data.timeframe}</p>

                    <br>

                    <h3>DIRECTION</h3>

                    <p>${data.direction}</p>

                </div>


                <div class="strategy-info">

                    <h3 class="bullish-text">BULLISH SETUP</h3>

                    <p>${data.bullish}</p>

                    <br>

                    <h3 class="bearish-text">BEARISH SETUP</h3>

                    <p>${data.bearish}</p>

                </div>


                <div class="strategy-info">

                    <h3>STOP LOSS</h3>

                    <p>${data.stop}</p>

                    <br>

                    <h3>TAKE PROFIT</h3>

                    <p>${data.target}</p>

                </div>

            </div>


            <div class="strategy-warning">

                <strong>IMPORTANT:</strong>
                ${data.warning}

            </div>

        `;


        const panel = document.getElementById("strategyDetail");

        panel.classList.add("active");

        panel.scrollIntoView({

            behavior: "smooth",

            block: "start"

        });
        startStrategyAnimation(type);

    }


    function closeStrategy() {

        document.getElementById("strategyDetail")
            .classList.remove("active");

    }
// ============================================================
// ANIMATED STRATEGY ENGINE
// ============================================================

let strategyAnimationFrame = null;


function createStrategyCandles(direction) {

    const candles = [];

    const sign = direction === "BULLISH" ? 1 : -1;

    let price = 100;

    for (let i = 0; i < 44; i++) {

        let movement = 0;

        // Initial market movement
        if (i < 14) {

            movement = -sign * 0.18;

        }

        // Liquidity sweep
        else if (i === 14) {

            movement = -sign * 1.1;

        }

        // Strong displacement
        else if (i <= 23) {

            movement = sign * 0.65;

        }

        // Retracement
        else if (i <= 30) {

            movement = -sign * 0.38;

        }

        // Confirmation
        else if (i === 31) {

            movement = sign * 0.65;

        }

        // Movement towards target
        else {

            movement = sign * 0.52;

        }

        movement += Math.sin(i * 1.7) * 0.10;

        const open = price;

        const close = price + movement;

        let high = Math.max(open, close) + 0.12;

        let low = Math.min(open, close) - 0.12;


        // Extend sweep wick
        if (i === 14) {

            if (sign === 1) {

                low -= 0.8;

            } else {

                high += 0.8;

            }

        }

        candles.push({

            open: open,
            close: close,
            high: high,
            low: low

        });

        price = close;

    }

    return candles;

}


function drawStrategyChart(canvas, type, direction, visible) {

    if (!canvas) return;

    const ctx = canvas.getContext("2d");

    const width = canvas.clientWidth;

    const height = canvas.clientHeight;

    if (!width || !height) return;

    const dpr = window.devicePixelRatio || 1;

    canvas.width = width * dpr;

    canvas.height = height * dpr;

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    ctx.clearRect(0, 0, width, height);


    const candles = createStrategyCandles(direction);

    const sign = direction === "BULLISH" ? 1 : -1;

    const sweep = candles[14];

    const zoneCandles = candles.slice(27, 31);

    const zoneHigh = Math.max(
        ...zoneCandles.map(c => c.high)
    );

    const zoneLow = Math.min(
        ...zoneCandles.map(c => c.low)
    );

    const entry = candles[31].close;

    const stop = sign === 1
        ? sweep.low - 0.35
        : sweep.high + 0.35;

    const target = entry + sign * 3.8;


    const allPrices = candles.flatMap(c => [
        c.high,
        c.low
    ]);

    allPrices.push(stop, target, entry);

    const minPrice = Math.min(...allPrices) - 0.5;

    const maxPrice = Math.max(...allPrices) + 0.5;


    const left = 45;

    const right = 90;

    const top = 30;

    const bottom = 35;

    const chartWidth = width - left - right;

    const chartHeight = height - top - bottom;


    function x(index) {

        return left + (index / 44) * chartWidth;

    }


    function y(price) {

        return top +
            ((maxPrice - price) / (maxPrice - minPrice))
            * chartHeight;

    }


    // Background grid

    ctx.strokeStyle = "rgba(255,255,255,0.07)";

    ctx.lineWidth = 1;

    for (let i = 0; i <= 5; i++) {

        const gy = top + (chartHeight / 5) * i;

        ctx.beginPath();

        ctx.moveTo(left, gy);

        ctx.lineTo(width - right, gy);

        ctx.stroke();

    }


    // Draw candles

    const candleWidth = Math.max(
        4,
        chartWidth / 44 * 0.55
    );


    for (let i = 0; i < Math.min(visible, candles.length); i++) {

        const c = candles[i];

        const bullish = c.close >= c.open;

        const color = bullish ? "#00D68F" : "#FF5263";

        const cx = x(i);

        ctx.strokeStyle = color;

        ctx.fillStyle = color;

        ctx.lineWidth = 1.5;


        // Wick

        ctx.beginPath();

        ctx.moveTo(cx, y(c.high));

        ctx.lineTo(cx, y(c.low));

        ctx.stroke();


        // Candle body

        const bodyTop = Math.min(
            y(c.open),
            y(c.close)
        );

        const bodyHeight = Math.max(
            2,
            Math.abs(y(c.open) - y(c.close))
        );

        ctx.fillRect(
            cx - candleWidth / 2,
            bodyTop,
            candleWidth,
            bodyHeight
        );

    }


    // Draw setup annotations only when reached

    function drawLine(price, color, label, dashed = false) {

        const lineY = y(price);

        ctx.save();

        ctx.strokeStyle = color;

        ctx.fillStyle = color;

        ctx.lineWidth = 1.5;

        ctx.setLineDash(dashed ? [6, 5] : []);

        ctx.beginPath();

        ctx.moveTo(left, lineY);

        ctx.lineTo(width - right, lineY);

        ctx.stroke();

        ctx.setLineDash([]);

        ctx.font = "bold 11px Arial";

        ctx.fillText(
            label,
            width - right + 8,
            lineY - 5
        );

        ctx.restore();

    }


    // Liquidity sweep

    if (visible > 15) {

        const sweepPrice = sign === 1
            ? sweep.low
            : sweep.high;

        ctx.fillStyle = "#D6AD60";

        ctx.font = "bold 11px Arial";

        ctx.fillText(
            sign === 1 ? "SELL-SIDE SWEEP" : "BUY-SIDE SWEEP",
            x(14) - 30,
            y(sweepPrice) + (sign === 1 ? 18 : -12)
        );

    }


    // Strategy zone

    if (visible > 25) {

        const zoneX = x(26);

        const zoneWidth = x(32) - zoneX;

        ctx.fillStyle = "rgba(0,184,255,0.18)";

        ctx.fillRect(
            zoneX,
            y(zoneHigh),
            zoneWidth,
            Math.abs(y(zoneLow) - y(zoneHigh))
        );

        ctx.strokeStyle = "#00B8FF";

        ctx.strokeRect(
            zoneX,
            y(zoneHigh),
            zoneWidth,
            Math.abs(y(zoneLow) - y(zoneHigh))
        );

        ctx.fillStyle = "#00B8FF";

        ctx.font = "bold 11px Arial";

        let zoneLabel = "ENTRY ZONE";

        if (type === "orderblock") {
            zoneLabel = "ORDER BLOCK";
        }

        if (type === "fvg") {
            zoneLabel = "FAIR VALUE GAP";
        }

        if (type === "liquidity") {
            zoneLabel = "REACTION ZONE";
        }

        ctx.fillText(
            zoneLabel,
            zoneX,
            y(zoneHigh) - 8
        );

    }


    // Entry, stop loss and target

    if (visible > 32) {

        drawLine(
            entry,
            "#00B8FF",
            "ENTRY"
        );

        drawLine(
            stop,
            "#FF5263",
            "STOP LOSS"
        );

        drawLine(
            target,
            "#00D68F",
            "TAKE PROFIT"
        );

    }


    // Confirmation marker

    if (visible > 32) {

        ctx.fillStyle = "#FFFFFF";

        ctx.font = "bold 11px Arial";

        ctx.fillText(
            "CONFIRMATION",
            x(31) - 35,
            y(entry) - 20
        );

    }


    // Show RR information

    if (visible > 32) {

        ctx.fillStyle = "#D6AD60";

        ctx.font = "bold 12px Arial";

        ctx.fillText(
            "R:R  1:2",
            left + 8,
            top + 15
        );

    }


    // Display current animation status

    const status = document.getElementById("strategyStatus");

    if (status) {

        let message = "ANALYSING MARKET...";

        if (visible > 14) {
            message = "LIQUIDITY SWEPT";
        }

        if (visible > 23) {
            message = "DISPLACEMENT CONFIRMED";
        }

        if (visible > 29) {
            message = "PRICE RETRACING";
        }

        if (visible > 32) {
            message = "ENTRY CONFIRMED";
        }

        if (visible >= 44) {
            message = "TAKE PROFIT HIT";
        }

        status.textContent = message;

        status.style.color =
            visible >= 44 ? "#00D68F" : "#00B8FF";

    }

}


function startStrategyAnimation(type) {

    if (strategyAnimationFrame) {

        cancelAnimationFrame(strategyAnimationFrame);

    }

    const canvas = document.getElementById("strategyChart");

    if (!canvas) return;


    const cycleDuration = 11000;

    let startTime = null;


    function animate(timestamp) {

        if (!startTime) {

            startTime = timestamp;

        }

        const elapsed = timestamp - startTime;

        const cycle = Math.floor(elapsed / cycleDuration);

        const cycleTime = elapsed % cycleDuration;


        // Alternate bullish and bearish setups

        const direction = cycle % 2 === 0
            ? "BULLISH"
            : "BEARISH";


        const visible = Math.min(
            44,
            Math.floor(cycleTime / 200)
        );


        drawStrategyChart(
            canvas,
            type,
            direction,
            visible
        );


        strategyAnimationFrame =
            requestAnimationFrame(animate);

    }


    strategyAnimationFrame =
        requestAnimationFrame(animate);

}

    </script>

    """

    return render_page(content)
# ============================================================
# OFFICIAL BROKER APPS PAGE
# ============================================================

@app.route("/platforms")
def platforms():

    content = """

    <style>

        .platform-hero {
            padding: 100px 9%;
            background: linear-gradient(120deg, #07111F, #05080D);
            text-align: center;
        }

        .platform-hero h1 {
            font-size: clamp(38px, 6vw, 65px);
            margin-bottom: 20px;
        }

        .platform-hero h1 span {
            color: #00B8FF;
        }

        .platform-hero p {
            color: #AAB7C5;
            max-width: 650px;
            margin: auto;
            line-height: 1.8;
        }

        .platform-section {
            padding: 75px 9%;
        }

        .broker-grid {
            display: grid;
            grid-template-columns:
                repeat(auto-fit, minmax(280px, 1fr));
            gap: 30px;
        }

        .broker-card {
            background: #0B1726;
            border: 1px solid rgba(0,184,255,0.2);
            border-radius: 15px;
            padding: 35px;
            transition: 0.3s;
        }

        .broker-card:hover {
            transform: translateY(-6px);
            border-color: #00B8FF;
            box-shadow: 0 15px 35px rgba(0,184,255,0.12);
        }

        .broker-label {
            color: #D6AD60;
            letter-spacing: 3px;
            font-size: 12px;
            margin-bottom: 20px;
        }

        .broker-card h2 {
            font-size: 32px;
            margin-bottom: 15px;
        }

        .broker-card > p {
            color: #AAB7C5;
            line-height: 1.8;
            margin-bottom: 25px;
        }

        .download-option {
            background: #07111F;
            padding: 20px;
            border-radius: 9px;
            margin-top: 15px;
            border: 1px solid rgba(255,255,255,0.06);
        }

        .download-option h3 {
            font-size: 17px;
            margin-bottom: 8px;
        }

        .download-option p {
            color: #91A0B0;
            font-size: 13px;
            line-height: 1.6;
            margin-bottom: 15px;
        }

        .download-btn {
            display: block;
            text-align: center;
            padding: 13px;
            background: #00B8FF;
            color: #05080D;
            text-decoration: none;
            font-weight: bold;
            border-radius: 5px;
            transition: 0.3s;
        }

        .download-btn:hover {
            background: #FFFFFF;
        }

        .broker-note {
            margin-top: 30px;
            padding: 20px;
            border-left: 3px solid #D6AD60;
            background: rgba(214,173,96,0.07);
            color: #AAB7C5;
            line-height: 1.8;
            font-size: 13px;
        }

        .platform-disclaimer {
            text-align: center;
            padding: 30px 9%;
            color: #8293A5;
            font-size: 12px;
            line-height: 1.8;
        }

    </style>


    <section class="platform-hero">

        <div class="strategy-label">
            ELITE FOREX ACADEMY / TRADING PLATFORMS
        </div>

        <h1>
            YOUR TRADING.
            <span>YOUR PLATFORM.</span>
        </h1>

        <p>
            Access the official trading applications
            from our supported brokers.

            Download your preferred platform and
            access the financial markets from
            your mobile device or computer.
        </p>

    </section>


    <section class="platform-section">

        <div class="broker-grid">


            <!-- EXNESS -->

            <div class="broker-card">

                <div class="broker-label">
                    OFFICIAL BROKER PLATFORM
                </div>

                <h2>Exness</h2>

                <p>
                    Access Exness trading services through
                    its official applications and
                    MetaTrader trading platforms.
                </p>


                <div class="download-option">

                    <h3>Exness Trade App</h3>

                    <p>
                        Access your Exness account,
                        manage funds and trade supported
                        MT5 accounts.
                    </p>

                    <a
                        href="https://www.exness.com/exness-trade-app/"
                        target="_blank"
                        rel="noopener noreferrer"
                        class="download-btn">

                        DOWNLOAD EXNESS APP →

                    </a>

                </div>


                <div class="download-option">

                    <h3>MetaTrader 5</h3>

                    <p>
                        Download the official Exness
                        MT5 platform for supported
                        mobile and desktop devices.
                    </p>

                    <a
                        href="https://www.exness.com/metatrader-5-app/"
                        target="_blank"
                        rel="noopener noreferrer"
                        class="download-btn">

                        DOWNLOAD EXNESS MT5 →

                    </a>

                </div>


                <div class="broker-note">

                    Always select the correct Exness
                    trading server when logging into
                    MetaTrader 5.

                </div>

            </div>



            <!-- XM -->

            <div class="broker-card">

                <div class="broker-label">
                    OFFICIAL BROKER PLATFORM
                </div>

                <h2>XM</h2>

                <p>
                    Access XM trading services, open your trading
                    account and download the official applications.
                </p>

                <!-- CREATE XM ACCOUNT -->

                <div class="download-option">

                    <h3>Open XM Trading Account</h3>

                    <p>
                        Register for an XM trading account through
                        our partner registration link.
                    </p>

                <a
                    href="/xm-redirect"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="download-btn">

                    CREATE XM ACCOUNT →

                </a>

            </div>


            <!-- XM MOBILE APP -->

            <div class="download-option">

                <h3>XM App</h3>

            <p>
                Access XM services through its official
                mobile application.
            </p>

            <a
                href="https://clicks.pipaffiliates.com/c?c=1347361&l=en&p=17"
                target="_blank"
                rel="noopener noreferrer"
                class="download-btn">

                DOWNLOAD XM APP →

            </a>
        </div>
        <!-- XM ADVANCED MATERIAL LEARNING -->

<div class="download-option">

    <h3>Advanced Material Learning</h3>

    <p>
        Access XM educational resources and advanced
        trading learning materials.
    </p>

    <a
        href="https://clicks.pipaffiliates.com/c?c=1347361&l=en&p=7"
        target="_blank"
        rel="noopener noreferrer"
        class="download-btn">

        ADVANCED MATERIAL LEARNING →

    </a>

</div>


        <!-- XM MT5 -->

        <div class="download-option">

            <h3>MetaTrader 5</h3>

            <p>
                Access the official XM MT5 download options
                for mobile, desktop and web.
            </p>

            <a
                href="https://www.xm.com/mt5"
                target="_blank"
                rel="noopener noreferrer"
                class="download-btn">

                DOWNLOAD XM MT5 →

            </a>

        </div>


        <div class="broker-note">

            Use your XM MT5 account credentials and the
            correct XM server when logging into MetaTrader 5.

        </div>

    </div>

</section>


    <section class="platform-disclaimer">

        ELITE FOREX ACADEMY provides educational
        information and links to official broker
        platforms.

        Trading involves significant risk.
        Downloading an application does not guarantee
        trading success or profitability.

        Always verify the application publisher
        before installation.

    </section>

    """

    return render_page(content)


# ============================================================
# ABOUT PAGE
# ============================================================

@app.route("/about")

def about():

    content = """

    <section class="hero">

        <div class="hero-content">

            <div class="hero-label">ABOUT ELITE FOREX ACADEMY</div>

            <h1>

                BUILT FOR

                <span>MARKET KNOWLEDGE.</span>

            </h1>

            <p class="hero-description">

                Elite Forex Academy is focused on

                educating traders about Smart Money

                Concepts, ICT methodologies and

                institutional price action.

            </p>

        </div>

    </section>


    <section class="section">

        <div class="section-heading">

            <small>OUR MISSION</small>

            <h2>Education. Discipline. Precision.</h2>

            <p>

                Our mission is to make structured trading

                education accessible and help individuals

                understand the complexity of financial markets.

            </p>

        </div>

    </section>

    """

    return render_page(content)


# ============================================================
# XM ACCOUNT PAGE
# ============================================================

@app.route("/open-account")

def open_account():

    content = """

    <section class="hero">

        <div class="hero-content">

            <div class="hero-label">ELITE FOREX ACADEMY / PARTNER</div>

            <h1>

                BEGIN YOUR

                <span>TRADING JOURNEY.</span>

            </h1>


            <p class="hero-description">

                Explore XM as a trading platform.

                Review its account conditions, available

                instruments, fees and risks before deciding

                whether to open an account.

            </p>


            <div class="hero-buttons">

                <a href="/xm-redirect" class="primary-button">

                    CREATE XM ACCOUNT

                </a>


                <a href="/smc" class="secondary-button">

                    EXPLORE EDUCATION

                </a>

            </div>

        </div>

    </section>


    <section class="affiliate-section">

        <h2>

            TRADE WITH <span>KNOWLEDGE.</span>

        </h2>


        <p>

            Opening a trading account is a personal decision.

            Make sure you understand the risks involved in

            leveraged forex and CFD trading before depositing

            money or placing trades.

        </p>

    </section>

    """

    return render_page(content)


# ============================================================
# XM AFFILIATE REDIRECT
# ============================================================

@app.route("/xm-redirect")

def xm_redirect():

    if not XM_REFERRAL_LINK:

        return """

        <h2>XM affiliate link not configured.</h2>

        <p>Please configure your XM IB referral link.</p>

        <a href="/open-account">Go back</a>

        """, 503


    return redirect(XM_REFERRAL_LINK)


# ============================================================
# ERROR HANDLING
# ============================================================

@app.errorhandler(404)

def page_not_found(error):

    return render_page("""

        <section class="hero">

            <div class="hero-content">

                <h1>404 <span>PAGE NOT FOUND</span></h1>

                <p class="hero-description">

                    The page you are looking for does not exist.

                </p>

                <a href="/" class="primary-button">

                    RETURN HOME

                </a>

            </div>

        </section>

    """), 404


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    print("=" * 60)

    print("ELITE FOREX ACADEMY")

    print("=" * 60)

    print("Website running at:")

    print("http://127.0.0.1:5001")

    print("=" * 60)

    app.run(

        host="127.0.0.1",

        port=5001,

        debug=False

    )