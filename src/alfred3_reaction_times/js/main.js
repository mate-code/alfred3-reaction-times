const eventNamespaces = {
    sequencePart: "art.sequencePart",
    trial: "art.trial",
    reactionTimes: "art.reactionTimes"
}

const events = {
    sequencePart: {
        namespace: "art.sequencePart",
        start: "art.sequencePart.start",
        finish: "art.sequencePart.finish",
    },
    trial: {
        namespace: "art.trial",
        start: "art.trial.start",
        finish: "art.trial.finish",
    },
    reactionTimes: {
        namespace: "art.reactionTimes",
        start: "art.reactionTimes.start",
        finish: "art.reactionTimes.finish",
    }
}

const types = {
    pause: "pause",
    fixation: "fixation",
    stimulus: "stimulus",
    feedback: "feedback",
}

class AlfredSequenceExecutable {

    events = {
        start: "start",
        finish: "finish"
    }

    constructor(element, eventNamespace = "") {
        this.element = $(element)

        this.id = this.element.parent().parent().attr("id").slice(0, -("-container".length));

        this.eventNamespace = eventNamespace;
        if (this.eventNamespace && this.eventNamespace.slice(-1) !== ".") {
            this.eventNamespace += "."
        }
    }

    async promiseExecution() {
        this.start()
        await this.execute().then(() => {
            this.finish()
        })
    }

    start() {
        this.trigger(this.events.start)
    }

    /**
     * @returns {Promise<unknown>}
     */
    execute() {
    }

    finish() {
        this.trigger(this.events.finish)
    }

    on(event, callback) {
        this.element.on(this.eventNamespace + event, callback);
    }

    trigger(event, context) {
        context = typeof context === "undefined" ? this : context;
        this.element.trigger(this.eventNamespace + event, context);
    }

}

class ReactionTimes extends AlfredSequenceExecutable {

    pos

    constructor(element) {
        super(element, eventNamespaces.reactionTimes)

        this.trials = []
        this.element.find(".trial").each((i, trialElement) => {
            this.trials.push(new Trial(trialElement, this))
        });

        this.promiseExecution().then(() => {
            console.log("done")
        })
    }

    async execute() {
        for (this.pos = 0; this.pos < this.trials.length; this.pos++) {
            await this.trials[this.pos].promiseExecution()
        }
    }

}

class Trial extends AlfredSequenceExecutable {

    pos

    constructor(element, reactionTimes) {
        super(element, eventNamespaces.trial)
        this.reactionTimes = reactionTimes

        this.sequence = []
        this.element.find(".sequence-part").each((i, sequencePartElement) => {
            this.sequence.push(new SequencePart(sequencePartElement, this))
        });
    }

    start() {
        super.start();
        this.element.show()
    }

    async execute() {
        for (this.pos = 0; this.pos < this.sequence.length; this.pos++) {
            await this.sequence[this.pos].promiseExecution()
        }
    }

    finish() {
        super.finish();
        this.element.hide();
    }

}

const timer = ms => new Promise(res => setTimeout(res, ms))

const awaitClick = () => new Promise((res) => {
    let onClick = () => {
        console.log("clicked")
        $(document).off("click", onClick)
        res()
    }
    $(document).on("click", onClick)
})

class SequencePart extends AlfredSequenceExecutable {

    constructor(element, trial) {
        super(element, eventNamespaces.sequencePart)
        this.trial = trial

        this.duration = parseFloat(this.element.data("duration")) * 1000
        this.type = this.element.data("type")
    }

    start() {
        super.start();
        this.element.show()
    }

    execute() {
        return this.duration !== 0
            ? timer(this.duration)
            : awaitClick();
    }

    finish() {
        super.finish();
        this.element.hide();
    }

}

$(document).ready(function () {

    let reactionElements = $(".reactions");

    let includeEvents = [
        events.sequencePart.start,
        events.sequencePart.finish,
    ];
    $.each(events, (i, elementEvents) => {
        $.each(elementEvents, (i, eventName) => {
            if (includeEvents.length !== 0 && !includeEvents.includes(eventName)) {
                return null;
            }
            reactionElements.on(eventName, (e, context) => {
                console.log(eventName + " " + context.id);
            })
        });
    });

    reactionElements.each((i, element) => {
        new ReactionTimes(element);
    });

});