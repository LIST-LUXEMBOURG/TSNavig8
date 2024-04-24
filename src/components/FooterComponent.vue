<!-- 
  © 2024 - Luxembourg Institute of Science and Technology. All Rights Reserved
  This program is licensed under AGPL V3.0 License -  https://www.gnu.org/licenses/agpl-3.0.txt
-->
<template>
  <footer class="footer">
      <div class="d-flex flex-row justify-content-between align-items-center flex-grow-1">
        <img src="../assets/list_logo.png" alt="logo-list" class="footer-logo" height="40px"/>
        <p class="project-title">(C)2024 LEONE project</p>
        <img src="../assets/FNR_LOGO_Black.png" alt="logo-fnr" class="footer-logo" height="40px"/>
      </div>
  </footer>
</template>
<script setup>
</script>
<style scoped>
.footer {
  position: fixed;
  width: calc(100% - 24px);
  bottom: 0;
  padding: 30px 10px;
  color: black;
  border-top: 10px double #b8b4c3;
  background: #ffffff;
}

@media screen and (max-width: 1400px) {
  .footer {
    position: relative;
    width: calc(100% - 24px);
    padding: 30px 10px;
    color: black;
    border-top: 10px double #b8b4c3;
    background: #ffffff;
  }
}
.footer-logo {
  width: 200px;
}
.project-title {
  font-family: "Roboto", sans-serif;
  font-weight: 100;
  font-style: normal;
  margin: 0;
  padding: 0;
}
</style>

