<template>
  <div class="reports-view">
    <el-card class="reports-card">
      <template #header>
        <div class="card-header">
          <h2>Reports</h2>
          <el-button type="primary" @click="generateReport">Generate Report</el-button>
        </div>
      </template>

      <el-row :gutter="20">
        <el-col :span="24">
          <el-form :model="reportForm" label-width="120px">
            <el-form-item label="Report Type">
              <el-select v-model="reportForm.type" placeholder="Select report type">
                <el-option label="Project Progress" value="project_progress" />
                <el-option label="Task Completion" value="task_completion" />
                <el-option label="Team Performance" value="team_performance" />
                <el-option label="Time Tracking" value="time_tracking" />
              </el-select>
            </el-form-item>

            <el-form-item label="Date Range">
              <el-date-picker
                v-model="reportForm.dateRange"
                type="daterange"
                range-separator="to"
                start-placeholder="Start date"
                end-placeholder="End date"
              />
            </el-form-item>

            <el-form-item label="Format">
              <el-radio-group v-model="reportForm.format">
                <el-radio label="pdf">PDF</el-radio>
                <el-radio label="excel">Excel</el-radio>
                <el-radio label="csv">CSV</el-radio>
              </el-radio-group>
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="generateReport">Generate</el-button>
              <el-button @click="resetForm">Reset</el-button>
            </el-form-item>
          </el-form>
        </el-col>
      </el-row>

      <el-row :gutter="20" class="mt-4">
        <el-col :span="24">
          <el-card shadow="hover">
            <template #header>
              <div class="card-header">
                <h3>Recent Reports</h3>
              </div>
            </template>
            <el-table :data="recentReports" style="width: 100%">
              <el-table-column prop="name" label="Report Name" />
              <el-table-column prop="type" label="Type" />
              <el-table-column prop="generated_at" label="Generated At">
                <template #default="{ row }">
                  {{ formatDate(row.generated_at) }}
                </template>
              </el-table-column>
              <el-table-column prop="format" label="Format" />
              <el-table-column label="Actions">
                <template #default="{ row }">
                  <el-button-group>
                    <el-button type="primary" size="small" @click="downloadReport(row)">
                      Download
                    </el-button>
                    <el-button type="danger" size="small" @click="deleteReport(row)">
                      Delete
                    </el-button>
                  </el-button-group>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { formatDate } from '@/utils/date'

interface ReportForm {
  type: string
  dateRange: [Date, Date] | null
  format: string
}

const reportForm = ref<ReportForm>({
  type: '',
  dateRange: null,
  format: 'pdf'
})

const recentReports = ref([
  {
    name: 'Project Progress Report',
    type: 'Project Progress',
    generated_at: new Date(),
    format: 'PDF'
  },
  {
    name: 'Task Completion Report',
    type: 'Task Completion',
    generated_at: new Date(),
    format: 'Excel'
  }
])

const generateReport = async () => {
  try {
    if (!reportForm.value.type) {
      ElMessage.warning('Please select a report type')
      return
    }

    if (!reportForm.value.dateRange) {
      ElMessage.warning('Please select a date range')
      return
    }

    // TODO: Implement report generation logic
    ElMessage.success('Report generation started')
  } catch (error) {
    console.error('Error generating report:', error)
    ElMessage.error('Failed to generate report')
  }
}

const resetForm = () => {
  reportForm.value = {
    type: '',
    dateRange: null,
    format: 'pdf'
  }
}

const downloadReport = (report: any) => {
  // TODO: Implement report download logic
  ElMessage.success('Downloading report...')
}

const deleteReport = async (report: any) => {
  try {
    // TODO: Implement report deletion logic
    ElMessage.success('Report deleted successfully')
  } catch (error) {
    console.error('Error deleting report:', error)
    ElMessage.error('Failed to delete report')
  }
}
</script>

<style scoped lang="scss">
.reports-view {
  padding: 20px;

  .reports-card {
    margin-bottom: 20px;
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    h2, h3 {
      margin: 0;
    }
  }

  .mt-4 {
    margin-top: 20px;
  }
}
</style> 