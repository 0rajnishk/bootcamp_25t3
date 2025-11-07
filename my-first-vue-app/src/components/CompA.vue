<template>
    <div class="comp-a">
        <h1>component A</h1>
        <h2>{{ msg }}</h2>
        <button @click="sendToParent">send data</button>
    </div>
</template>

<script>
export default {
    data() {
        return {
            data: 'data from child'
        }
    },
    props: {
        msg: String
    },

    methods: {
        sendToParent() {
            this.$emit('send-data', this.data)
        }
    }
}

</script>