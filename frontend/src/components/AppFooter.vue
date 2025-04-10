<template>
  <div class="footer">
    <div class="footer-content">
      <div class="footer-section">
        <h3>{{ $t('footer.about') }}</h3>
        <p>{{ $t('footer.description') }}</p>
      </div>
      
      <div class="footer-section">
        <h3>{{ $t('footer.contact') }}</h3>
        <p>
          <el-icon><Message /></el-icon>
          support@se1dhe.dev
        </p>
        <p>
          <el-icon><Phone /></el-icon>
          +380 (XX) XXX-XX-XX
        </p>
      </div>
      
      <div class="footer-section">
        <h3>{{ $t('footer.social') }}</h3>
        <div class="social-links">
          <a href="#" target="_blank">
            <el-icon><Telegram /></el-icon>
          </a>
          <a href="#" target="_blank">
            <el-icon><Github /></el-icon>
          </a>
        </div>
      </div>
    </div>
    
    <div class="footer-bottom">
      <p>&copy; {{ new Date().getFullYear() }} Se1dhe Dev. {{ $t('footer.rights') }}</p>
    </div>
  </div>
</template>

<script>
import { Message, Phone, Telegram, Github } from '@element-plus/icons-vue'

export default {
  name: 'AppFooter',
  components: {
    Message,
    Phone,
    Telegram,
    Github
  }
}
</script>

<style lang="scss" scoped>
.footer {
  background-color: #2c3e50;
  color: white;
  padding: 40px 0 20px;
  
  .footer-content {
    display: flex;
    justify-content: space-around;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    
    .footer-section {
      flex: 1;
      margin: 0 20px;
      
      h3 {
        margin-bottom: 20px;
        font-size: 18px;
      }
      
      p {
        margin: 10px 0;
        
        .el-icon {
          margin-right: 10px;
        }
      }
      
      .social-links {
        display: flex;
        gap: 20px;
        
        a {
          color: white;
          font-size: 24px;
          
          &:hover {
            color: #ffd04b;
          }
        }
      }
    }
  }
  
  .footer-bottom {
    text-align: center;
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
  }
}

@media (max-width: 768px) {
  .footer-content {
    flex-direction: column;
    text-align: center;
    
    .footer-section {
      margin: 20px 0;
      
      .social-links {
        justify-content: center;
      }
    }
  }
}
</style> 