<script type='ts'>
    export let topic = 'An example found topic';
    $: topic

    let rand = () => {return Math.floor(Math.random()*255)}

    let gradient = `linear-gradient(45deg, rgb(${rand()},${rand()},${rand()}) 0%, rgb(${rand()},${rand()},${rand()}) 100%)`
    console.log(gradient)
    // let gradient = 'linear-gradient(45deg, rgba(255,0,0,1) 0%, rgba(0,255,229,1) 100%) '

</script>

<div class="outer" style='background: {gradient} !important;'>
    <div class="topic"><h3>{topic}</h3></div>
</div>



<style>
    .outer {
        --width: 20vw;
        --height: 10vh;
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
    }
    .topic {
        display: flex;
        align-items: center;
        justify-items: center;
        justify-content: center;
        text-align: center;
        border-radius: 10px;
        justify-self: center;
        width: calc(var(--width) - 5px);
        height: calc(var(--height) - 5px);
        background-color: rgba(28, 28, 33, .87);
    }
</style>