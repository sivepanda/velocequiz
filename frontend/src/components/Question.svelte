<script type="ts">
    export let question =
        {"content": "Which of the following security measures is not completely effective against attacks like phishing?","responses": [{"content": "A. 2FA", "correct": false}, {"content": "B. Enhanced Logging resources", "correct": false}, {"content": "C. Changing passwords of privileged accounts", "correct": false}, {"content": "D. All of the above", "correct": true}]};
    export let questionNumber = 1;
    export let showAnswer = false;

    var questionJSON = question;
    $: questionJSON = question;
    console.log(questionJSON.responses);
</script>

<div class="outer">
    <div class="question">{questionNumber}&period;&nbsp;{questionJSON.content}</div>
    <div class="responses">
        {#each questionJSON.responses as res}
            <span
                class="response {showAnswer ? 'showanswer' : 'noanswer'} {res.correct ? 'correct' : 'incorrect'}">
                {res.content}
                <span class="material-symbols-outlined">{res.correct ? 'check' : 'close'}</span>
            </span>
        {/each}
    </div>
</div>

<style>
    @media only print {
        .outer {
            width: 100% !important;
        }
        .question {
            width: 100% !important;
            box-shadow: none !important;
            padding: 0px !important;
        }
        .noanswer span {
            opacity: 0 !important;
            visibility: hidden;
        }
    }
    .outer {
        background-color: var(--midnight-400);
        width: 50vw;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        padding-bottom: 1vh;
        margin-bottom: 2vh;
        margin-top: 2vh;
    }
    .question {
        padding-left: 1vw;
        padding-right: 1vw;
        padding-top: 2vh;
        padding-bottom: 2vh;
        border-radius: 10px;
        width: 48vw;
        background-color: var(--midnight-350);
        font-family: var(--head);
        font-size: 2svh;

        box-shadow: 0px 1px 1px 1px rgba(0, 0, 0, 0.17);
    }
    .showanswer span {
        opacity: 1 !important;
        visibility: visible;
    }
    .responses {
        margin-left: 4vw;
        margin-top: 1vh;
        margin-bottom: 1vh;
        display: flex;
        flex-direction: column;
        width: 100%;
        font-family: var(--body);
    }
    .response {
        display: flex;
        padding-top: 1vh;
        padding-bottom: 1vh;
        flex-direction: row;
        align-items: center;
        gap: 4px;
    }
    .response span {
        opacity: 0;
        transition: all ease-in-out 100ms;
    }
    .response:hover span {
        opacity: 1;
        transition: all ease-in-out 200ms;
    }

    .correct,
    .correct:hover {
        color: var(--bermuda-250);
        transition: all ease-in-out 100ms;
    }
    .incorrect,
    .incorrect:hover {
        color: var(--clay-250);
        transition: all ease-in-out 100ms;
    }
    .noanswer {
        color: white;
        transition: all ease-in-out 100ms;
    }
</style>
