<template>
    <div>
        <h1>Welcome to the Home View {{ data1 }}</h1>
    </div>
    <button @click="popAlert()" >alert</button>
    <button @click="hello()" >fetch hello</button>
</template>

<script>
import axios from 'axios';


export default{

    data() {
        return{
            data1:'data1 value'
        }
    },
    methods: {

        async popAlert(){
            alert('Hello world!' + this.data1)
        },

        async hello(){
            // http://127.0.0.1:5000
            alert('inside hello')
            const response = await axios.get('http://127.0.0.1:5000');
            alert('api call ')
            console.log(response)
            alert(response.data.msg)
        }

        

    }

}


</script>


<style scoped>

</style>