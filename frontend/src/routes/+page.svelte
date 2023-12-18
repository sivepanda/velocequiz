<body class="page">
    <a href="/" class="titlenm">veloce<span class="logotype">quiz</span></a>
    <div class="types">
        <a href="/auto-quiz-builder" class="outer">
            <div class="topic">
                <span class="material-symbols-outlined"> smart_toy </span>
                <h3>Automatically build a quiz</h3>
            </div>
        </a>
        <a href="/quiz-builder" class="outer">
            <div class="topic">
                <span class="material-symbols-outlined"> edit_square </span>
                <h3>Build your own quiz</h3>
            </div>
        </a>
    </div>
</body>

<style>
    @import url('https://fonts.googleapis.com/css2?family=Dela+Gothic+One&family=Inter:wght@600&family=Open+Sans&display=swap');

    .page {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    a {
        all: unset;
    }
    .types {
        width: 70vw;
        height: 80vh;
        padding-left: 10vw;
        padding-right: 10vw;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
    }
    .outer {
        --width: 30vw;
        --height: 50vh;
        width: var(--width);
        height: var(--height);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-items: center;
        justify-content: center;
        border-radius: 10px;
        margin-bottom: 2vh;
        margin-top: 2vh;
        transition: 250ms all ease-in;
        cursor: pointer;
    }
    .outer:hover {
        transform: scale(1.1);
        transition: 250ms all ease-out;
    }
    .outer:first-of-type {
        background: linear-gradient(45deg, #fc466b, #3f5efb);
    }
    .outer:nth-of-type(2) {
        background: linear-gradient(45deg, #11998e, #38ef7d);
    }
    .topic {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-items: center;
        justify-content: center;
        text-align: center;
        border-radius: 10px;
        justify-self: center;
        width: calc(var(--width) - 5px);
        height: calc(var(--height) - 5px);
        background-color: rgba(28, 28, 33, 0.95);
        transition: 250ms all ease-in;
    }
    .outer:hover > .topic {
        background-color: rgba(28, 28, 33, 0.85);
        transition: 250ms all ease-out;
    }
    .topic > span {
        font-size: 15vh;
    }
</style>
