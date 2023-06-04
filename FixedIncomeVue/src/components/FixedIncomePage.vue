<template>
    <div class="common-layout">
        <el-container>
            <!-- aside -->
            <asideBar />

            <!-- Main page -->
            <indexTable />

        </el-container>
    </div>
</template>


<script>
import asideBar from "./asideBar.vue";
import indexTable from "./indexTable.vue";

export default {
    components: {
        asideBar,
        indexTable
    },

    data() {
        return {
        }
    },

    computed: {
    },

    methods: {
    },


    mounted() {
    },


}

</script>


<style></style>
