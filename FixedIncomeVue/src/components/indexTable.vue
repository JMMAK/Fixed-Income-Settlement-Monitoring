<template>
    <el-container>
        <el-header
            style="text-align: center; font-size: 12px; line-height: var(--el-header-height);padding-left: 0;padding-right: 0;">
            <el-row>
                <el-col :span="24">
                    <div class="grid-content ep-bg-purple-dark" style="background-color:#545c64;">
                        <el-text tag="b" size="large" style="color:#eebe77">Deal input</el-text>
                    </div>
                </el-col>
            </el-row>
        </el-header>


        <el-main style="background-color: antiquewhite;">


            <el-row>
                <el-col :span="3">
                    <el-text tag="b" class="mx-2">Entity</el-text>
                    <el-input v-model="inputData.entity" placeholder="Entity" />
                </el-col>

                <el-col :span="4">
                    <el-text tag="b" class="mx-2">Deal PTA</el-text>
                    <el-input v-model="inputData.pta" placeholder="Deal PTA" />
                </el-col>
                <!-- 7 -->
                <el-col :span="3">
                    <el-text tag="b" class="mx-2">ISIN</el-text>
                    <el-input v-model="inputData.isin" placeholder="ISIN" />
                </el-col>

                <el-col :span="3">
                    <el-text tag="b" class="mx-2">Deal Status</el-text>
                    <el-input v-model="inputData.status" placeholder="Deal Status" />
                </el-col>
                <!-- 13 -->

                <el-col :span="3">
                    <el-text tag="b" class="mx-2">Date</el-text>
                    <el-date-picker v-model="inputData.date" type="date" placeholder="Date" value-format="YYYY-MM-DD" />
                </el-col>
                <el-col :span="1">
                </el-col>
                <!-- 17 -->
                <el-col :span="2" style="line-height: var(--el-menu-item-height);margin: auto;">
                    <el-button type="success" style="margin: auto;" @click="search" round>Go</el-button>
                </el-col>
                <!-- 19 -->

                <el-col :span="4" style="line-height: var(--el-menu-item-height);margin: auto;">

                </el-col>
                <!-- 23 -->
                <el-col :span="1">
                </el-col>
            </el-row>

            <!-- Table -->
            <el-row>
                <el-col :span="24">
                    <el-scrollbar>
                        <el-table :data="dealTable" @selection-change="handleSelectionChange">
                            <el-table-column type="expand">
                                <template #default="props">
                                    <el-card class="box-card">
                                        <div m="4">
                                            <p m="t-0 b-2">Entity: {{ props.row.Entity }}</p>
                                            <p m="t-0 b-2">PTA: {{ props.row.PTA }}</p>
                                            <p m="t-0 b-2">ISIN: {{ props.row.ISIN }}</p>
                                            <p m="t-0 b-2">To BIC: {{ props.row.to_BIC }}</p>
                                            <p m="t-0 b-2">Sender BIC: {{ props.row.sender_BIC }}</p>
                                            <p m="t-0 b-2">Settelment Data: {{ props.row.settelment_Data }}</p>
                                            <p m="t-0 b-2">Matching status: {{ props.row.matching_status }}</p>
                                        </div>
                                    </el-card>
                                </template>
                            </el-table-column>

                            <el-table-column type="selection"></el-table-column>
                            <el-table-column prop="Entity" label="Entity" width="80" show-overflow-tooltip />
                            <el-table-column prop="PTA" label="Deal PTA" width="140" show-overflow-tooltip />
                            <el-table-column prop="ISIN" label="ISIN" width="180" show-overflow-tooltip />
                            <el-table-column prop="to_BIC" label="To BIC" width="100" show-overflow-tooltip />
                            <el-table-column prop="sender_BIC" label="Sender BIC" width="100" show-overflow-tooltip />
                            <el-table-column prop="settelment_Data" label="Settelment Data" width="100"
                                show-overflow-tooltip />
                            <el-table-column prop="matching_status" label="Matching status" width="130"
                                show-overflow-tooltip />

                            <el-table-column label="Operations" width="150">
                                <template #default="scope">
                                    <el-button size="small" type="danger"
                                        @click="handleAutomation(scope.$index, scope.row)">Automation</el-button>
                                </template>
                            </el-table-column>

                        </el-table>

                    </el-scrollbar>
                    <el-pagination v-model:current-page="currentPage" v-model:page-size="pageSize"
                        :page-sizes="[10, 50, 100, 200, 300, 400]" :small="small" :disabled="disabled"
                        :background="background" layout="total, sizes, prev, pager, next, jumper" :total="dealCount"
                        @size-change="handleSizeChange" @current-change="handleCurrentChange" />
                </el-col>

            </el-row>


        </el-main>
    </el-container>

    <el-dialog v-model="AutomationCenterDialogVisible" title="Automation FollowUp" width="30%" destroy-on-close center>
        <ul>
            <li>
                prediction percent: 66.66%
            </li>
            <li>
                Activities Time: 02 Jun 2023
            </li>
        </ul>
        <span>
            <h3>
                <strong>Exception: </strong>
            </h3>
        </span>
        <span>
            <h3>
                <strong>History: </strong>
            </h3>
            <ul>
                <li>
                    prediction percent: 66.66%
                </li>
                <li>
                    Activities Time: 01 Jun 2023
                </li>
            </ul>
        </span>
        <template #footer>
            <span class="dialog-footer">
                <el-button type="primary" @click="AutomationCenterDialogVisible = false">
                    Generate mail
                </el-button>
            </span>
        </template>
    </el-dialog>
</template>

<script>
// import { ref } from 'vue'
import axios from 'axios';

export default {

    data() {
        return {
            item: {
                date: '2016-05-02',
                name: 'Tom',
                address: 'No. 189, Grove St, Los Angeles',
            },

            inputData: {
                entity: '',
                pta: '',
                isin: '',
                status: '',
                date: ''

            },
            dealTable: [],

            AutomationCenterDialogVisible: false,

            // pagination
            currentPage: 1,
            pageSize: 50,
            small: false,
            disabled: false,
            background: false,
            dealCount: 0
        }
    },

    computed: {
        tableData() {
            // return Array.from({ length: 20 }).fill(this.item)
            return [{
                Entity: 'HK',
                PTA: '123456789012',
                ISIN: '123456789013',
                to_BIC: 'BICxxx',
                sender_BIC: 'BICxxx',
                settelment_Data: '2016-00-00',
                matching_status: 'FLP'

            },
            {
                Entity: 'HK',
                PTA: '123456789013',
                ISIN: '123456789013',
                to_BIC: 'BICxxx',
                sender_BIC: 'BICxxx',
                settelment_Data: '2016-00-00',
                matching_status: 'FLP'

            },]
        },
    },

    methods: {
        handleSelectionChange(deal) {
            console.log(deal)
        },
        handleAutomation(index, row) {
            console.log(index, row)
            this.AutomationCenterDialogVisible = true;
        },

        handleSizeChange(val) {
            console.log(`${val} items per page`)
            this.pageSize = val
            this.getdeals()
        },
        handleCurrentChange(val) {
            console.log(`current page: ${val}`)
            this.currentPage = val
            this.getdeals()
        },

        search() {
            console.log(this.inputData.date);
            this.getdeals()
        },

        getdeals() {
            axios({
                method: "get",
                url: '/api/V1/deals',
                params: {
                    page: this.currentPage,
                    pageSize: this.pageSize,
                    Entity: this.inputData.entity,
                    PTA: '',
                    ISIN: this.inputData.isin,
                    sender_BIC: '',
                    settelment_Data: this.inputData.date,
                    matching_status: this.inputData.status,
                }
            }).then(res => {
                this.dealTable = res.data;
            })
            this.getDealCount()
        },

        getDealCount() {
            axios({
            method: "get",
            url: '/api/V1/deals',
            params: {
                count: 1,
                page: this.currentPage,
                pageSize: this.pageSize,
                Entity: this.inputData.entity,
                PTA: '',
                ISIN: this.inputData.isin,
                sender_BIC: '',
                settelment_Data: this.inputData.date,
                matching_status: this.inputData.status,
            }
        }).then(res => {
            this.dealCount = res.data.dealCount;
        })
        }

    },


    mounted() {
        this.getdeals()
    },


}

</script>


<style>
.el-row {
    margin-bottom: 20px;
}

.el-date-editor.el-input,
.el-date-editor.el-input__wrapper {
    width: auto;
}
</style>
