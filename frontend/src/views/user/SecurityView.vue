<template>
  <div class="security">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>Security Settings</h2>
        </div>
      </template>

      <el-tabs v-model="activeTab">
        <el-tab-pane label="Password" name="password">
          <el-form
            ref="passwordFormRef"
            :model="passwordForm"
            :rules="passwordRules"
            label-width="120px"
            class="security-form"
          >
            <el-form-item label="Current Password" prop="currentPassword">
              <el-input
                v-model="passwordForm.currentPassword"
                type="password"
                show-password
                placeholder="Enter your current password"
              />
            </el-form-item>

            <el-form-item label="New Password" prop="newPassword">
              <el-input
                v-model="passwordForm.newPassword"
                type="password"
                show-password
                placeholder="Enter your new password"
              />
            </el-form-item>

            <el-form-item label="Confirm Password" prop="confirmPassword">
              <el-input
                v-model="passwordForm.confirmPassword"
                type="password"
                show-password
                placeholder="Confirm your new password"
              />
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                @click="handlePasswordChange"
                :loading="changingPassword"
              >
                Change Password
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="Two-Factor Auth" name="2fa">
          <div class="two-factor-auth">
            <div class="status-section">
              <h3>Two-Factor Authentication</h3>
              <el-switch
                v-model="twoFactorEnabled"
                @change="handleTwoFactorToggle"
                :loading="togglingTwoFactor"
              />
              <p class="status-text">
                {{ twoFactorEnabled ? 'Enabled' : 'Disabled' }}
              </p>
            </div>

            <div v-if="twoFactorEnabled" class="setup-section">
              <h4>Setup Instructions</h4>
              <ol>
                <li>Download an authenticator app (Google Authenticator, Authy, etc.)</li>
                <li>Scan the QR code below with your authenticator app</li>
                <li>Enter the 6-digit code from your authenticator app</li>
              </ol>

              <div class="qr-code">
                <!-- TODO: Add QR code component -->
                <div class="qr-placeholder">QR Code will be displayed here</div>
              </div>

              <el-form
                ref="verificationFormRef"
                :model="verificationForm"
                :rules="verificationRules"
                label-width="120px"
                class="verification-form"
              >
                <el-form-item label="Verification Code" prop="code">
                  <el-input
                    v-model="verificationForm.code"
                    placeholder="Enter 6-digit code"
                    maxlength="6"
                  />
                </el-form-item>

                <el-form-item>
                  <el-button
                    type="primary"
                    @click="handleVerification"
                    :loading="verifying"
                  >
                    Verify
                  </el-button>
                </el-form-item>
              </el-form>
            </div>
          </div>
        </el-tab-pane>

        <el-tab-pane label="Sessions" name="sessions">
          <div class="sessions">
            <h3>Active Sessions</h3>
            <el-table :data="activeSessions" style="width: 100%">
              <el-table-column prop="device" label="Device" />
              <el-table-column prop="location" label="Location" />
              <el-table-column prop="lastActive" label="Last Active" />
              <el-table-column label="Actions" width="120">
                <template #default="{ row }">
                  <el-button
                    type="danger"
                    link
                    @click="handleTerminateSession(row.id)"
                    :loading="terminatingSession === row.id"
                  >
                    Terminate
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'

const activeTab = ref('password')
const changingPassword = ref(false)
const togglingTwoFactor = ref(false)
const verifying = ref(false)
const terminatingSession = ref<number | null>(null)
const twoFactorEnabled = ref(false)

const passwordFormRef = ref<FormInstance>()
const verificationFormRef = ref<FormInstance>()

const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const verificationForm = reactive({
  code: ''
})

const passwordRules = {
  currentPassword: [
    { required: true, message: 'Please enter your current password', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: 'Please enter your new password', trigger: 'blur' },
    { min: 8, message: 'Password must be at least 8 characters', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: 'Please confirm your new password', trigger: 'blur' },
    {
      validator: (rule: any, value: string, callback: Function) => {
        if (value !== passwordForm.newPassword) {
          callback(new Error('Passwords do not match'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

const verificationRules = {
  code: [
    { required: true, message: 'Please enter the verification code', trigger: 'blur' },
    { pattern: /^\d{6}$/, message: 'Code must be 6 digits', trigger: 'blur' }
  ]
}

const activeSessions = ref([
  {
    id: 1,
    device: 'Chrome on MacOS',
    location: 'San Francisco, CA',
    lastActive: '2 minutes ago'
  },
  {
    id: 2,
    device: 'Safari on iPhone',
    location: 'San Francisco, CA',
    lastActive: '1 hour ago'
  }
])

const handlePasswordChange = async () => {
  if (!passwordFormRef.value) return
  
  await passwordFormRef.value.validate(async (valid) => {
    if (valid) {
      changingPassword.value = true
      try {
        // TODO: Implement API call to change password
        ElMessage.success('Password changed successfully')
        passwordForm.currentPassword = ''
        passwordForm.newPassword = ''
        passwordForm.confirmPassword = ''
      } catch (error) {
        console.error('Error changing password:', error)
        ElMessage.error('Failed to change password')
      } finally {
        changingPassword.value = false
      }
    }
  })
}

const handleTwoFactorToggle = async (value: string | number | boolean) => {
  togglingTwoFactor.value = true
  try {
    // TODO: Implement API call to toggle 2FA
    ElMessage.success(`Two-factor authentication ${value ? 'enabled' : 'disabled'}`)
  } catch (error) {
    console.error('Error toggling 2FA:', error)
    ElMessage.error('Failed to toggle two-factor authentication')
    twoFactorEnabled.value = !value // Revert the toggle
  } finally {
    togglingTwoFactor.value = false
  }
}

const handleVerification = async () => {
  if (!verificationFormRef.value) return
  
  await verificationFormRef.value.validate(async (valid) => {
    if (valid) {
      verifying.value = true
      try {
        // TODO: Implement API call to verify 2FA code
        ElMessage.success('Two-factor authentication verified')
      } catch (error) {
        console.error('Error verifying 2FA:', error)
        ElMessage.error('Failed to verify two-factor authentication')
      } finally {
        verifying.value = false
      }
    }
  })
}

const handleTerminateSession = async (sessionId: number) => {
  terminatingSession.value = sessionId
  try {
    // TODO: Implement API call to terminate session
    ElMessage.success('Session terminated')
    activeSessions.value = activeSessions.value.filter(session => session.id !== sessionId)
  } catch (error) {
    console.error('Error terminating session:', error)
    ElMessage.error('Failed to terminate session')
  } finally {
    terminatingSession.value = null
  }
}
</script>

<style scoped lang="scss">
.security {
  padding: 20px;

  .card-header {
    h2 {
      margin: 0;
    }
  }

  .security-form {
    max-width: 500px;
    margin-top: 20px;
  }

  .two-factor-auth {
    .status-section {
      display: flex;
      align-items: center;
      gap: 16px;
      margin-bottom: 32px;

      h3 {
        margin: 0;
      }

      .status-text {
        margin: 0;
        color: var(--el-text-color-secondary);
      }
    }

    .setup-section {
      max-width: 500px;

      h4 {
        margin-bottom: 16px;
      }

      ol {
        margin-bottom: 24px;
        padding-left: 20px;
      }

      .qr-code {
        width: 200px;
        height: 200px;
        margin: 24px 0;
        background-color: var(--el-border-color-light);
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 4px;

        .qr-placeholder {
          color: var(--el-text-color-secondary);
        }
      }

      .verification-form {
        margin-top: 24px;
      }
    }
  }

  .sessions {
    h3 {
      margin-bottom: 24px;
    }
  }
}
</style> 