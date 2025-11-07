<template>
    <div>
        <h1>Welcome to the Home View {{ data }}</h1>

        <p>{{ user.username }}</p>
        <p>{{ user.email }}</p>
        <p>{{ user.phone_number }}</p>

        <!-- Child component: listen for the custom event 'send-data' emitted by CompA -->
        <CompA :msg="data" @send-data="ChildData" />

        <p>Child says: {{ dataA }}</p>

        <button @click="popAlert()">alert</button>
        <button @click="hello()">fetch hello</button>
    </div>
</template>

<script>
import axios from 'axios';
import CompA from '@/components/CompA.vue';

export default{

    data() {
        return{
            data:'data value',
            dataA: 'waiting..',
            user:{}
        }
    },
    components:{ 
        CompA
    },
    methods: {

        popAlert(){
            alert('Hello world! ' + this.data)
        },

        async hello(){
            const token = localStorage.getItem('token')
            const response = await axios.get('http://127.0.0.1:5000/register', {
                headers:{
                    Authorization: `Bearer ${token}`
                }
            });
            alert('api call ')
            console.log(response)
            this.user = response.data.user
            alert(response.data.msg)
        },
        ChildData(data) {
            // show and store the payload coming from CompA
            alert('received from child: ' + data)
            this.dataA = data
        }

        

    },
    mounted() {
        this.hello()
    }

}

</script>


<style scoped>

</style>