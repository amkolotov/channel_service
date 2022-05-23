<template>
    <div class="wrapper">
      <Header />
      <Content />

    </div>
</template>


<script setup>
import Header from '@/components/Header.vue'
import Content from '@/components/Content.vue'
</script>

<style>
  .total-col {
    display: flex;
    justify-content: center;
  }

  .total {
    width: 300px;
    border: 1px #e2e2e2 solid;
    margin-bottom: 10px;
  }
  .total-header {
    background-color: black;
    color: white;
    text-align: center;
  }
  .total-content {
    height: 100px;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .total-result {
    font-size: 50px;
  }

  .table {
    width: 100%;
  }

  .table th {
    color: white;
    background-color: black;
    text-align: center;
  }

  .table td {
    background-color: #e8f1fe;
    border: 1px solid #e2e2e2;
    text-align: end;
  }
</style>
