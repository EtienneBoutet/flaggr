<template>
  <div class="header-container">
    <b-tag
      :class="{'points': true, 'is-solved': challenge.is_solved, 'is-unsolved': !challenge.is_solved }"
      size="is-medium"
    >{{ challenge.points }}</b-tag>
    <p class="card-header-title">
      {{ challenge.name }}
      <b-icon v-if="challenge.is_solved" icon="check" type="is-solved" size="is-medium"></b-icon>
    </p>

    <a class="card-header-icon">
      <b-icon :icon="open ? 'chevron-down' : 'chevron-up'" size="is-medium"></b-icon>
    </a>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { Challenge } from '@/models/challenge'

/**
 * Header of the challenge card
 */
export default Vue.extend({
  name: 'ChallengeCardHeader',
  props: {
    challenge: Challenge,
    open: Boolean
  }
});
</script>

<style lang="scss">
@import "../style/theme.scss";

.header-container {
    width: 100%;
    display: flex;
    font-family: $secondary-font;

    .card-header-title {
        font-weight: 400;
        font-size: 1.1rem;

      .icon {
        margin-left: 0.5rem;

        .mdi-light:before {
          color: inherit;
        }
      }
    }

    .points {
        margin: 0.75rem 0;
        font-weight: 600;
    }
}
</style>
