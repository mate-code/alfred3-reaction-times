/**
 * Event namespaces for reaction time alfred3 elements
 * @type {{reaction: string, sequencePart: string, reactionTimes: string, trial: string}}
 */
const eventNamespaces = {
    reactionTimes: "art.reactionTimes",
    trial: "art.trial",
    sequencePart: "art.sequencePart",
    reaction: "art.reaction",
}

/**
 * Available types of SequencePart objects
 * @type {{feedback: string, stimulus: string, fixation: string, pause: string}}
 */
const types = {
    pause: "pause",
    fixation: "fixation",
    stimulus: "stimulus",
    feedback: "feedback",
}

/**
 * Available suffixes for stimulus input names
 * @type {{reaction: string, time: string}}
 */
const inputs = {
    reaction: "reaction",
    time: "time"
}

/**
 * Object representing an alfred3 elements html.
 * Implements on() and trigger() methods as shortcuts for the corresponding jQuery methods
 */
class AlfredElement {

    /**
     * @param {jQuery} element jQuery representation of the alfred3 element
     * @param {string} eventNamespace namespace key as noted in const eventNamespaces
     */
    constructor(element, eventNamespace) {
        this.element = $(element)
        this.id = this.element.attr("id")

        this.eventNamespace = eventNamespace
        if (!this.eventNamespace) this.eventNamespace = ""
        else if (this.eventNamespace.slice(-1) !== ".") this.eventNamespace += "."
    }

    /**
     * @param {string} event event name (will be prefixed by namespace if set)
     * @param {function} callback function to call on event trigger
     */
    on(event, callback) {
        this.element.on(this.eventNamespace + event, callback)
    }

    /**
     * @param {string} event event name (will be prefixed by namespace if set)
     * @param {object=} context contextual object to pass to triggered function
     */
    trigger(event, context) {
        context = typeof context === "undefined" ? this : context
        this.element.trigger(this.eventNamespace + event, context)
    }

}

/**
 * Alfred3 element that can be executed in a sequence
 */
class AlfredExecutableSequenceElement extends AlfredElement {

    /**
     * Events triggered during execution
     * @type {{start: string, finish: string}}
     */
    events = {
        start: "start",
        finish: "finish"
    }

    /**
     * Triggers events and executes the promise of the element
     * @returns {Promise<void>}
     */
    async execute() {
        this.start()
        await this.promise().then(() => {
            this.finish()
        })
    }

    /**
     * Triggers the start event.
     * Can be extended to add behaviour to the element.
     */
    start() {
        this.trigger(this.events.start)
    }

    /**
     * Must be extended with a returned promise that executes the element
     * @returns {Promise<unknown>}
     */
    promise() {
        return new Promise((res) => res())
    }

    /**
     * Triggers the finish event.
     * Can be extended to add behaviour to the element.
     */
    finish() {
        this.trigger(this.events.finish)
    }

}

/**
 * Handles the execution of trials
 */
class ReactionTimes extends AlfredExecutableSequenceElement {

    /**
     * Current position in the execution of trials
     */
    pos

    /**
     * @param {jQuery} element representation of ReactionTimes element
     */
    constructor(element) {
        super(element, eventNamespaces.reactionTimes)

        this.allImagesLoaded().then(() => {
            let maxHeight = 0
            this.trials = []
            this.element.find(".trial").each((i, trialElement) => {
                trialElement = $(trialElement)
                this.trials.push(new Trial(trialElement, this))
                if(trialElement.height() > maxHeight) maxHeight = trialElement.height()
            });
            this.element.css("height", maxHeight + "px")
            this.execute()
        })
    }

    /**
     * Promise to wait for all images to be fully loaded
     */
    async allImagesLoaded() {
        let loadPromises = []
        this.element.find("img").each((i, imageElement) => {
            loadPromises.push(new Promise(res => {
                $("<img>").on("load", () => res()).attr("src", $(imageElement).attr("src"))
            }))
        })
        await Promise.all(loadPromises)
    }

    /**
     * Iterate through promises of trials
     * @returns {Promise<void>}
     */
    async promise() {
        for (this.pos = 0; this.pos < this.trials.length; this.pos++) {
            await this.trials[this.pos].execute()
        }
    }

}

/**
 * Handles the execution of sequence parts
 */
class Trial extends AlfredExecutableSequenceElement {

    /**
     * Current position in the execution of sequence parts
     */
    pos

    /**
     * @param {jQuery} element representation of Trial element
     * @param {ReactionTimes} reactionTimes parent ReactionTimes object that handles this trial
     */
    constructor(element, reactionTimes) {
        super(element, eventNamespaces.trial)
        this.reactionTimes = reactionTimes

        let maxHeight = 0
        this.sequence = []
        this.element.find(".sequence-part").each((i, sequencePartElement) => {
            sequencePartElement = $(sequencePartElement)
            this.sequence.push(new SequencePart(sequencePartElement, this))
            if(sequencePartElement.height() > maxHeight) maxHeight = sequencePartElement.height()
        });
        this.element.css("height", maxHeight + "px")
    }

    /**
     * Extension of start event
     */
    start() {
        super.start();
        this.element.css("visibility", "inherit")
    }

    /**
     * Iterate through sequence parts of trials
     * @returns {Promise<void>}
     */
    async promise() {
        for (this.pos = 0; this.pos < this.sequence.length; this.pos++) {
            await this.sequence[this.pos].execute()
        }
    }

    /**
     * Extension of finish event
     */
    finish() {
        super.finish();
        this.element.css("visibility", "hidden")
    }

}

/**
 * Handles the execution of a SequencePart
 */
class SequencePart extends AlfredExecutableSequenceElement {

    /**
     * @param {jQuery} element representation of SequencePart element
     * @param {Trial} trial parent Trial object that handles the execution of this part
     */
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

    /**
     * Extension of start event
     */
    start() {
        super.start();
        this.element.css("visibility", "inherit")
    }

    /**
     * Merge promises to Promise.any
     * This includes duration/timeouts and (for stimuli) possible user reactions.
     * Meeting any of these promises will continue the execution of the parent trial
     */
    promise() {
        let promises = []

        if(this.duration !== 0) {
            promises.push(this._timer(this.duration))
        }
        this.reactions.forEach(reaction => {
            promises.push(reaction.promise())
        })

        return Promise.any(promises)
    }

    /**
     * Extension of finish event
     */
    finish() {
        super.finish();
        this.element.css("visibility", "hidden")
    }

    /**
     * Find hidden input element (stimuli only)
     * @param {string} name
     * @returns {null|jQuery|HTMLElement|*}
     */
    findInput(name) {
        if(this.type !== types.stimulus) return null
        let inputName = this.element.data("input-" + name)
        if(!inputName) return null
        return $(`[name="${inputName}"]`)
    }

    /**
     * Read value of hidden input element (stimuli only)
     * @param {string} name
     * @returns {null|*}
     */
    readInput(name) {
        let input = this.findInput(name)
        if(!input) return null
        return input.attr("value")
    }

    /**
     * Write value of hidden input element (stimuli only)
     * @param {string} name
     * @param value
     * @returns {null|*}
     */
    writeInput(name, value) {
        let input = this.findInput(name)
        if(!input) return null
        input.attr("value", value)
    }

    /**
     * Timeout promise for handling durations and timeouts
     * @param {int} ms time in milliseconds
     * @returns {Promise<unknown>}
     * @private
     */
    _timer(ms) {
        return new Promise(res => setTimeout(() => {
            if(!this.readInput(inputs.reaction) || !this.readInput(inputs.time)) {
                this.writeInput(inputs.reaction, "--TIMEOUT--")
            }
            res()
        }, ms))
    }

}

/**
 * Representation of possible reaction to a stimulus
 */
class Reaction extends AlfredElement {

    /**
     * events to trigger
     * @type {{triggered: string}}
     */
    events = {
        triggered: "triggered",
    }
    /**
     * start time of reaction time measurement
     * @type {number}
     */
    start = 0
    /**
     * end time of reaction time measurement
     * @type {number}
     */
    end = 0

    /**
     *
     * @param element
     * @param sequencePart
     */
    constructor(element, sequencePart) {
        super(element, eventNamespaces.reaction);
        this.sequencePart = sequencePart

        this.key = parseInt(this.element.data("key"))
    }

    /**
     * Handles binding of onkeydown event to measure and write reaction
     * @returns {Promise<unknown>}
     */
    promise() {
        return new Promise(res => {
            let onKeydown = (e) => {
                if(this.key && e.which !== this.key) {
                    return null
                }
                this.end = performance.now()
                this.sequencePart.writeInput(inputs.reaction, this.id)
                this.sequencePart.writeInput(inputs.time, this.end - this.start)
                this.trigger(this.events.triggered)
                res()
            }
            this.start = performance.now()
            $(document).on("keydown", onKeydown)

            this.sequencePart.on(
                this.sequencePart.events.finish,
                () => $(document).off("keydown", onKeydown)
            )
        })
    }

}

$(document).ready(function () {

    $(".reaction-times").each((i, element) => {
        new ReactionTimes(element);
    });

});