<template>
  <div class="settings">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>Settings</h2>
        </div>
      </template>

      <el-tabs v-model="activeTab">
        <el-tab-pane label="General" name="general">
          <el-form
            ref="generalFormRef"
            :model="generalForm"
            :rules="generalRules"
            label-width="120px"
            class="settings-form"
          >
            <el-form-item label="Language" prop="language">
              <el-select v-model="generalForm.language" placeholder="Select language">
                <el-option label="English" value="en" />
                <el-option label="Russian" value="ru" />
                <el-option label="Spanish" value="es" />
                <el-option label="French" value="fr" />
                <el-option label="German" value="de" />
              </el-select>
            </el-form-item>

            <el-form-item label="Theme" prop="theme">
              <el-select v-model="generalForm.theme" placeholder="Select theme">
                <el-option label="Light" value="light" />
                <el-option label="Dark" value="dark" />
                <el-option label="System" value="system" />
              </el-select>
            </el-form-item>

            <el-form-item label="Time Zone" prop="timezone">
              <el-select v-model="generalForm.timezone" placeholder="Select time zone">
                <el-option label="UTC" value="UTC" />
                <el-option label="EST" value="EST" />
                <el-option label="PST" value="PST" />
                <el-option label="GMT" value="GMT" />
              </el-select>
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="handleGeneralSubmit" :loading="saving">
                Save Changes
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="Notifications" name="notifications">
          <el-form
            ref="notificationsFormRef"
            :model="notificationsForm"
            label-width="200px"
            class="settings-form"
          >
            <el-form-item label="Email Notifications">
              <el-switch v-model="notificationsForm.emailEnabled" />
            </el-form-item>

            <el-form-item label="Project Updates">
              <el-switch v-model="notificationsForm.projectUpdates" />
            </el-form-item>

            <el-form-item label="Task Assignments">
              <el-switch v-model="notificationsForm.taskAssignments" />
            </el-form-item>

            <el-form-item label="Task Due Dates">
              <el-switch v-model="notificationsForm.taskDueDates" />
            </el-form-item>

            <el-form-item label="Task Comments">
              <el-switch v-model="notificationsForm.taskComments" />
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="handleNotificationsSubmit" :loading="saving">
                Save Changes
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="Privacy" name="privacy">
          <el-form
            ref="privacyFormRef"
            :model="privacyForm"
            label-width="200px"
            class="settings-form"
          >
            <el-form-item label="Profile Visibility">
              <el-select v-model="privacyForm.profileVisibility" placeholder="Select visibility">
                <el-option label="Public" value="public" />
                <el-option label="Private" value="private" />
                <el-option label="Team Only" value="team" />
              </el-select>
            </el-form-item>

            <el-form-item label="Activity Feed">
              <el-select v-model="privacyForm.activityFeedVisibility" placeholder="Select visibility">
                <el-option label="Public" value="public" />
                <el-option label="Private" value="private" />
                <el-option label="Team Only" value="team" />
              </el-select>
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="handlePrivacySubmit" :loading="saving">
                Save Changes
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const activeTab = ref('general')
const saving = ref(false)

const generalFormRef = ref()
const generalForm = reactive({
  language: 'en',
  theme: 'light',
  timezone: 'UTC'
})

const generalRules = {
  language: [
    { required: true, message: 'Please select a language', trigger: 'change' }
  ],
  theme: [
    { required: true, message: 'Please select a theme', trigger: 'change' }
  ],
  timezone: [
    { required: true, message: 'Please select a time zone', trigger: 'change' }
  ]
}

const notificationsFormRef = ref()
const notificationsForm = reactive({
  emailEnabled: true,
  projectUpdates: true,
  taskAssignments: true,
  taskDueDates: true,
  taskComments: true
})

const privacyFormRef = ref()
const privacyForm = reactive({
  profileVisibility: 'private',
  activityFeedVisibility: 'team'
})

const handleGeneralSubmit = async () => {
  if (!generalFormRef.value) return

  try {
    await generalFormRef.value.validate()
    saving.value = true
    // TODO: Implement API call to save general settings
    ElMessage.success('General settings updated successfully')
  } catch (error) {
    console.error('Error updating general settings:', error)
    ElMessage.error('Failed to update general settings')
  } finally {
    saving.value = false
  }
}

const handleNotificationsSubmit = async () => {
  if (!notificationsFormRef.value) return

  try {
    await notificationsFormRef.value.validate()
    saving.value = true
    // TODO: Implement API call to save notification settings
    ElMessage.success('Notification settings updated successfully')
  } catch (error) {
    console.error('Error updating notification settings:', error)
    ElMessage.error('Failed to update notification settings')
  } finally {
    saving.value = false
  }
}

const handlePrivacySubmit = async () => {
  if (!privacyFormRef.value) return

  try {
    await privacyFormRef.value.validate()
    saving.value = true
    // TODO: Implement API call to save privacy settings
    ElMessage.success('Privacy settings updated successfully')
  } catch (error) {
    console.error('Error updating privacy settings:', error)
    ElMessage.error('Failed to update privacy settings')
  } finally {
    saving.value = false
  }
}
</script>

<style scoped lang="scss">
.settings {
  padding: 20px;

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    h2 {
      margin: 0;
    }
  }

  .settings-form {
    max-width: 600px;
    margin: 20px 0;
  }
}
</style> 