const eventNamespaces = {
    reactionTimes: "art.reactionTimes",
    trial: "art.trial",
    sequencePart: "art.sequencePart",
    reaction: "art.reaction",
}

const types = {
    pause: "pause",
    fixation: "fixation",
    stimulus: "stimulus",
    feedback: "feedback",
}

class AlfredElement {

    constructor(element, eventNamespace) {
        this.element = $(element)
        this.id = this.element.attr("id")

        this.eventNamespace = eventNamespace
        if (!this.eventNamespace) this.eventNamespace = ""
        else if (this.eventNamespace.slice(-1) !== ".") this.eventNamespace += "."
    }

    on(event, callback) {
        this.element.on(this.eventNamespace + event, callback)
    }

    trigger(event, context) {
        context = typeof context === "undefined" ? this : context
        this.element.trigger(this.eventNamespace + event, context)
    }

}

class AlfredExecutableSequenceElement extends AlfredElement {

    events = {
        start: "start",
        finish: "finish"
    }

    async execute() {
        this.start()
        await this.promise().then(() => {
            this.finish()
        })
    }

    start() {
        this.trigger(this.events.start)
    }

    /**
     * @returns {Promise<unknown>}
     */
    promise() {
        return new Promise((res) => res())
    }

    finish() {
        this.trigger(this.events.finish)
    }

}

class ReactionTimes extends AlfredExecutableSequenceElement {

    pos

    constructor(element) {
        super(element, eventNamespaces.reactionTimes)

        this.trials = []
        this.element.find(".trial").each((i, trialElement) => {
            this.trials.push(new Trial(trialElement, this))
        });
    }

    async promise() {
        for (this.pos = 0; this.pos < this.trials.length; this.pos++) {
            await this.trials[this.pos].execute()
        }
    }

}

class Trial extends AlfredExecutableSequenceElement {

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

    async promise() {
        for (this.pos = 0; this.pos < this.sequence.length; this.pos++) {
            await this.sequence[this.pos].execute()
        }
    }

    finish() {
        super.finish();
        this.element.hide();
    }

}

class SequencePart extends AlfredExecutableSequenceElement {

    constructor(element, trial) {
        super(element, eventNamespaces.sequencePart)
        this.trial = trial

        this.duration = parseFloat(this.element.data("duration")) * 1000
        this.type = this.element.data("type")

        this.reactions = []
        this.element.find(".reaction").each((i, reactionElement) => {
            this.reactions.push(new Reaction(reactionElement, this))
        });
    }

    start() {
        super.start();
        this.element.show()
    }

    promise() {
        let promises = []

        if(this.duration !== 0) {
            promises.push(this.timer(this.duration))
        }
        this.reactions.forEach(reaction => {
            promises.push(reaction.promise())
        })

        return  Promise.any(promises)
    }

    finish() {
        super.finish();
        this.element.hide();
    }

    timer(ms) {
        return new Promise(res => setTimeout(res, ms))
    }

}

class Reaction extends AlfredElement {

    events = {
        triggered: "triggered",
    }

    constructor(element, sequencePart) {
        super(element, eventNamespaces.reaction);
        this.sequencePart = sequencePart

        this.key = parseInt(this.element.data("key"))
    }

    promise() {
        return new Promise(res => {
            let onKeydown = (e) => {
                if(this.key && e.which !== this.key) {
                    return null
                }
                this.trigger(this.events.triggered)
                res()
            }
            $(document).on("keydown", onKeydown)

            this.sequencePart.on(
                this.sequencePart.events.finish,
                () => $(document).off("keydown", onKeydown)
            )
        })
    }

}


function bindEventDebugDisplay() {
    let events = {
        reactionTimes: {
            namespace: "art.reactionTimes",
            start: "art.reactionTimes.start",
            finish: "art.reactionTimes.finish",
        },
        trial: {
            namespace: "art.trial",
            start: "art.trial.start",
            finish: "art.trial.finish",
        },
        sequencePart: {
            namespace: "art.sequencePart",
            start: "art.sequencePart.start",
            finish: "art.sequencePart.finish",
        },
        reaction: {
            namespace: "art.reaction",
            triggered: "art.reaction.triggered",
        }
    }

    let includeEvents = [
        events.sequencePart.start,
        events.sequencePart.finish,
        events.reactionTimes.finish,
    ]

    let reactionElements = $(".reaction-times");
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
}

$(document).ready(function () {

    bindEventDebugDisplay()

    $(".reaction-times").each((i, element) => {
        new ReactionTimes(element).execute();
    });

});