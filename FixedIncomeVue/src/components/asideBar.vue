<template>
    <!-- aside -->
    <el-aside :width="aside_width">
        <el-scrollbar>
            <el-menu default-active="1" class="el-menu-vertical-demo" :collapse="isCollapse" @open="" @close=""
                @click="isCollapse = !isCollapse">
                <el-sub-menu index="1">
                    <template #title>
                        <el-icon>
                            <Operation />
                        </el-icon>
                        <span>Navigator</span>
                    </template>
                    <el-menu-item index="1-1">Deal Input</el-menu-item>
                    <el-menu-item index="1-2">item two</el-menu-item>

                </el-sub-menu>
            </el-menu>
        </el-scrollbar>

    </el-aside>
</template>

<script>
export default {
    data() {
        return {
            isCollapse: true,
        }
    },

    computed: {
        aside_width() {
            return this.isCollapse ? 'auto' : '200px'
        },
    }

}
</script>