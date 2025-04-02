<template>
  <div class="home">
    <el-row class="hero">
      <el-col :span="24">
        <h1>Добро пожаловать в SE1DHE Development</h1>
        <p>Платформа для разработки и управления проектами</p>
        <el-button type="primary" size="large" @click="$router.push('/register')">
          Начать работу
        </el-button>
      </el-col>
    </el-row>

    <el-row class="features">
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>Управление проектами</span>
            </div>
          </template>
          <div class="card-content">
            <p>Эффективное управление проектами и задачами</p>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>Аналитика</span>
            </div>
          </template>
          <div class="card-content">
            <p>Подробная аналитика и отчеты</p>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>Интеграции</span>
            </div>
          </template>
          <div class="card-content">
            <p>Интеграция с популярными сервисами</p>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
// Компонент использует только шаблон
</script>

<style scoped>
.home {
  padding: 2rem;
}

.hero {
  text-align: center;
  padding: 4rem 0;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  border-radius: 8px;
  margin-bottom: 2rem;
}

.hero h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.hero p {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 2rem;
}

.features {
  margin-top: 2rem;
}

.card-header {
  font-weight: bold;
}

.card-content {
  text-align: center;
  padding: 1rem 0;
}
</style> 