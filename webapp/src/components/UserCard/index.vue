<template>
  <div :class="['connect-user-card', {'connect-user-card--floats' : float}]">
    <div>
      <div class="connect-user-card-info">
        <Avatar />
        <div class="connect-user-card-info-text">
          <h3>{{user.name}}</h3>
          <p>{{user.position}}</p>
        </div>
      </div>
      <ul class="connect-user-card-options">
        <li @click="emitSound">
          <svg
            v-if="sound"
            width="18"
            height="18"
            viewBox="0 0 18 18"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M2.625 10.125H3.375V9C3.375 5.89837 5.89837 3.375 9 3.375C12.1016 3.375 14.625 5.89837 14.625 9V10.125H15.375V9C15.375 5.48475 12.5152 2.625 9 2.625C5.48475 2.625 2.625 5.48475 2.625 9V10.125Z"
              fill="#4F4F4F"
            />
            <path
              d="M16.125 15.375C17.1589 15.375 18 14.5339 18 13.5C18 12.4661 17.1589 11.625 16.125 11.625V12.375C16.7453 12.375 17.25 12.8798 17.25 13.5C17.25 14.1203 16.7453 14.625 16.125 14.625V15.375Z"
              fill="#4F4F4F"
            />
            <path
              d="M14.25 17.25H15C15.8272 17.25 16.5 16.5772 16.5 15.75V11.25C16.5 10.4227 15.8272 9.75 15 9.75H14.25C13.4227 9.75 12.75 10.4227 12.75 11.25V15.75C12.75 16.5772 13.4227 17.25 14.25 17.25ZM15 10.5C15.4136 10.5 15.75 10.8364 15.75 11.25V15.75C15.75 16.1636 15.4136 16.5 15 16.5H14.25C13.8364 16.5 13.5 16.1636 13.5 15.75V11.25C13.5 10.8364 13.8364 10.5 14.25 10.5H15Z"
              fill="#4F4F4F"
            />
            <path
              d="M1.875 15.375V14.625C1.25475 14.625 0.75 14.1203 0.75 13.5C0.75 12.8798 1.25475 12.375 1.875 12.375V11.625C0.841125 11.625 0 12.4661 0 13.5C0 14.5339 0.841125 15.375 1.875 15.375Z"
              fill="#4F4F4F"
            />
            <path
              d="M3.375 17.25C4.40887 17.25 5.25 16.4089 5.25 15.375V11.625C5.25 10.5911 4.40887 9.75 3.375 9.75C2.34112 9.75 1.5 10.5911 1.5 11.625V15.375C1.5 16.4089 2.34112 17.25 3.375 17.25ZM3.375 10.5C3.99525 10.5 4.5 11.0047 4.5 11.625V15.375C4.5 15.9952 3.99525 16.5 3.375 16.5C2.75475 16.5 2.25 15.9952 2.25 15.375V11.625C2.25 11.0047 2.75475 10.5 3.375 10.5Z"
              fill="#4F4F4F"
            />
          </svg>

          <svg
            v-else
            width="18"
            height="18"
            viewBox="0 0 18 18"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <g clip-path="url(#clip0)">
              <path
                d="M2.625 10.125H3.375V9C3.375 5.89837 5.89837 3.375 9 3.375C12.1016 3.375 14.625 5.89837 14.625 9V10.125H15.375V9C15.375 5.48475 12.5152 2.625 9 2.625C5.48475 2.625 2.625 5.48475 2.625 9V10.125Z"
                fill="#4F4F4F"
              />
              <path
                d="M16.125 15.375C17.1589 15.375 18 14.5339 18 13.5C18 12.4661 17.1589 11.625 16.125 11.625V12.375C16.7453 12.375 17.25 12.8798 17.25 13.5C17.25 14.1203 16.7453 14.625 16.125 14.625V15.375Z"
                fill="#4F4F4F"
              />
              <path
                d="M14.25 17.25H15C15.8272 17.25 16.5 16.5772 16.5 15.75V11.25C16.5 10.4227 15.8272 9.75 15 9.75H14.25C13.4227 9.75 12.75 10.4227 12.75 11.25V15.75C12.75 16.5772 13.4227 17.25 14.25 17.25ZM15 10.5C15.4136 10.5 15.75 10.8364 15.75 11.25V15.75C15.75 16.1636 15.4136 16.5 15 16.5H14.25C13.8364 16.5 13.5 16.1636 13.5 15.75V11.25C13.5 10.8364 13.8364 10.5 14.25 10.5H15Z"
                fill="#4F4F4F"
              />
              <path
                d="M1.875 15.375V14.625C1.25475 14.625 0.75 14.1203 0.75 13.5C0.75 12.8798 1.25475 12.375 1.875 12.375V11.625C0.841125 11.625 0 12.4661 0 13.5C0 14.5339 0.841125 15.375 1.875 15.375Z"
                fill="#4F4F4F"
              />
              <path
                d="M3.375 17.25C4.40887 17.25 5.25 16.4089 5.25 15.375V11.625C5.25 10.5911 4.40887 9.75 3.375 9.75C2.34112 9.75 1.5 10.5911 1.5 11.625V15.375C1.5 16.4089 2.34112 17.25 3.375 17.25ZM3.375 10.5C3.99525 10.5 4.5 11.0047 4.5 11.625V15.375C4.5 15.9952 3.99525 16.5 3.375 16.5C2.75475 16.5 2.25 15.9952 2.25 15.375V11.625C2.25 11.0047 2.75475 10.5 3.375 10.5Z"
                fill="#4F4F4F"
              />
              <line x1="16.386" y1="1.31785" x2="2.38597" y2="18.3179" stroke="#4F4F4F" />
            </g>
            <defs>
              <clipPath id="clip0">
                <rect width="18" height="18" transform="matrix(-1 0 0 1 18 0)" fill="white" />
              </clipPath>
            </defs>
          </svg>
        </li>
        <li @click="emitMicro">
          <svg
            v-if="micro"
            width="18"
            height="18"
            viewBox="0 0 18 18"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M8.74512 14.25C11.4331 14.25 13.6201 12.063 13.6201 9.375V4.875C13.6201 2.187 11.4331 0 8.74512 0C6.05712 0 3.87012 2.187 3.87012 4.875V9.375C3.87012 12.063 6.05712 14.25 8.74512 14.25ZM8.74512 0.75C11.0195 0.75 12.8701 2.60062 12.8701 4.875V9.375C12.8701 11.6494 11.0195 13.5 8.74512 13.5C6.47074 13.5 4.62012 11.6494 4.62012 9.375V4.875C4.62012 2.60062 6.47074 0.75 8.74512 0.75Z"
              fill="#4F4F4F"
            />
            <path
              d="M8.74512 15.75C12.3196 15.75 15.1201 12.9499 15.1201 9.375V7.875C15.1201 7.77554 15.0806 7.68016 15.0103 7.60983C14.94 7.53951 14.8446 7.5 14.7451 7.5C14.6457 7.5 14.5503 7.53951 14.48 7.60983C14.4096 7.68016 14.3701 7.77554 14.3701 7.875V9.375C14.3701 12.5291 11.8992 15 8.74512 15C5.59099 15 3.12012 12.5291 3.12012 9.375V7.875C3.12012 7.77554 3.08061 7.68016 3.01028 7.60983C2.93996 7.53951 2.84457 7.5 2.74512 7.5C2.64566 7.5 2.55028 7.53951 2.47995 7.60983C2.40963 7.68016 2.37012 7.77554 2.37012 7.875V9.375C2.37012 12.9499 5.17062 15.75 8.74512 15.75Z"
              fill="#4F4F4F"
            />
            <path d="M9.12012 15.375H8.37012V18H9.12012V15.375Z" fill="#4F4F4F" />
            <path
              d="M8.74512 3C8.84457 3 8.93996 2.96049 9.01028 2.89016C9.08061 2.81984 9.12012 2.72446 9.12012 2.625V0.375C9.12012 0.275544 9.08061 0.180161 9.01028 0.109835C8.93996 0.0395088 8.84457 0 8.74512 0C8.64566 0 8.55028 0.0395088 8.47995 0.109835C8.40963 0.180161 8.37012 0.275544 8.37012 0.375V2.625C8.37012 2.72446 8.40963 2.81984 8.47995 2.89016C8.55028 2.96049 8.64566 3 8.74512 3Z"
              fill="#4F4F4F"
            />
            <path
              d="M7.24512 2.99998C7.34457 2.99998 7.43996 2.96047 7.51028 2.89014C7.58061 2.81982 7.62012 2.72443 7.62012 2.62498V0.631103C7.62012 0.531647 7.58061 0.436265 7.51028 0.365938C7.43996 0.295612 7.34457 0.256104 7.24512 0.256104C7.14566 0.256104 7.05028 0.295612 6.97995 0.365938C6.90962 0.436265 6.87012 0.531647 6.87012 0.631103V2.62498C6.87012 2.72443 6.90962 2.81982 6.97995 2.89014C7.05028 2.96047 7.14566 2.99998 7.24512 2.99998Z"
              fill="#4F4F4F"
            />
            <path
              d="M10.2451 2.99998C10.3446 2.99998 10.44 2.96047 10.5103 2.89014C10.5806 2.81982 10.6201 2.72443 10.6201 2.62498V0.631103C10.6201 0.531647 10.5806 0.436265 10.5103 0.365938C10.44 0.295612 10.3446 0.256104 10.2451 0.256104C10.1457 0.256104 10.0503 0.295612 9.97995 0.365938C9.90963 0.436265 9.87012 0.531647 9.87012 0.631103V2.62498C9.87012 2.72443 9.90963 2.81982 9.97995 2.89014C10.0503 2.96047 10.1457 2.99998 10.2451 2.99998Z"
              fill="#4F4F4F"
            />
            <path d="M14.7451 9H2.74512V9.75H14.7451V9Z" fill="#4F4F4F" />
            <path
              d="M10.2451 5.25H13.2451C13.3446 5.25 13.44 5.21049 13.5103 5.14016C13.5806 5.06984 13.6201 4.97446 13.6201 4.875C13.6201 4.77554 13.5806 4.68016 13.5103 4.60984C13.44 4.53951 13.3446 4.5 13.2451 4.5H10.2451C10.1457 4.5 10.0503 4.53951 9.97995 4.60984C9.90963 4.68016 9.87012 4.77554 9.87012 4.875C9.87012 4.97446 9.90963 5.06984 9.97995 5.14016C10.0503 5.21049 10.1457 5.25 10.2451 5.25Z"
              fill="#4F4F4F"
            />
            <path
              d="M10.2451 6.75H13.2451C13.3446 6.75 13.44 6.71049 13.5103 6.64017C13.5806 6.56984 13.6201 6.47446 13.6201 6.375C13.6201 6.27554 13.5806 6.18016 13.5103 6.10983C13.44 6.03951 13.3446 6 13.2451 6H10.2451C10.1457 6 10.0503 6.03951 9.97995 6.10983C9.90963 6.18016 9.87012 6.27554 9.87012 6.375C9.87012 6.47446 9.90963 6.56984 9.97995 6.64017C10.0503 6.71049 10.1457 6.75 10.2451 6.75Z"
              fill="#4F4F4F"
            />
            <path
              d="M4.24512 5.25H7.24512C7.34457 5.25 7.43996 5.21049 7.51028 5.14016C7.58061 5.06984 7.62012 4.97446 7.62012 4.875C7.62012 4.77554 7.58061 4.68016 7.51028 4.60984C7.43996 4.53951 7.34457 4.5 7.24512 4.5H4.24512C4.14566 4.5 4.05028 4.53951 3.97995 4.60984C3.90963 4.68016 3.87012 4.77554 3.87012 4.875C3.87012 4.97446 3.90963 5.06984 3.97995 5.14016C4.05028 5.21049 4.14566 5.25 4.24512 5.25Z"
              fill="#4F4F4F"
            />
            <path
              d="M4.24512 6.75H7.24512C7.34457 6.75 7.43996 6.71049 7.51028 6.64017C7.58061 6.56984 7.62012 6.47446 7.62012 6.375C7.62012 6.27554 7.58061 6.18016 7.51028 6.10983C7.43996 6.03951 7.34457 6 7.24512 6H4.24512C4.14566 6 4.05028 6.03951 3.97995 6.10983C3.90963 6.18016 3.87012 6.27554 3.87012 6.375C3.87012 6.47446 3.90963 6.56984 3.97995 6.64017C4.05028 6.71049 4.14566 6.75 4.24512 6.75Z"
              fill="#4F4F4F"
            />
            <path
              d="M10.2451 8.25H13.2451C13.3446 8.25 13.44 8.21049 13.5103 8.14016C13.5806 8.06984 13.6201 7.97446 13.6201 7.875C13.6201 7.77554 13.5806 7.68016 13.5103 7.60983C13.44 7.53951 13.3446 7.5 13.2451 7.5H10.2451C10.1457 7.5 10.0503 7.53951 9.97995 7.60983C9.90963 7.68016 9.87012 7.77554 9.87012 7.875C9.87012 7.97446 9.90963 8.06984 9.97995 8.14016C10.0503 8.21049 10.1457 8.25 10.2451 8.25Z"
              fill="#4F4F4F"
            />
            <path
              d="M4.24512 8.25H7.24512C7.34457 8.25 7.43996 8.21049 7.51028 8.14016C7.58061 8.06984 7.62012 7.97446 7.62012 7.875C7.62012 7.77554 7.58061 7.68016 7.51028 7.60983C7.43996 7.53951 7.34457 7.5 7.24512 7.5H4.24512C4.14566 7.5 4.05028 7.53951 3.97995 7.60983C3.90963 7.68016 3.87012 7.77554 3.87012 7.875C3.87012 7.97446 3.90963 8.06984 3.97995 8.14016C4.05028 8.21049 4.14566 8.25 4.24512 8.25Z"
              fill="#4F4F4F"
            />
          </svg>

          <svg
            v-else
            width="18"
            height="18"
            viewBox="0 0 18 18"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <g clip-path="url(#clip0)">
              <path
                d="M8.74512 14.25C11.4331 14.25 13.6201 12.063 13.6201 9.375V4.875C13.6201 2.187 11.4331 0 8.74512 0C6.05712 0 3.87012 2.187 3.87012 4.875V9.375C3.87012 12.063 6.05712 14.25 8.74512 14.25ZM8.74512 0.75C11.0195 0.75 12.8701 2.60062 12.8701 4.875V9.375C12.8701 11.6494 11.0195 13.5 8.74512 13.5C6.47074 13.5 4.62012 11.6494 4.62012 9.375V4.875C4.62012 2.60062 6.47074 0.75 8.74512 0.75Z"
                fill="#4F4F4F"
              />
              <path
                d="M8.74512 15.75C12.3196 15.75 15.1201 12.9499 15.1201 9.375V7.875C15.1201 7.77554 15.0806 7.68016 15.0103 7.60983C14.94 7.53951 14.8446 7.5 14.7451 7.5C14.6457 7.5 14.5503 7.53951 14.48 7.60983C14.4096 7.68016 14.3701 7.77554 14.3701 7.875V9.375C14.3701 12.5291 11.8992 15 8.74512 15C5.59099 15 3.12012 12.5291 3.12012 9.375V7.875C3.12012 7.77554 3.08061 7.68016 3.01028 7.60983C2.93996 7.53951 2.84457 7.5 2.74512 7.5C2.64566 7.5 2.55028 7.53951 2.47995 7.60983C2.40963 7.68016 2.37012 7.77554 2.37012 7.875V9.375C2.37012 12.9499 5.17062 15.75 8.74512 15.75Z"
                fill="#4F4F4F"
              />
              <path d="M9.12012 15.375H8.37012V18H9.12012V15.375Z" fill="#4F4F4F" />
              <path
                d="M8.74512 3C8.84457 3 8.93996 2.96049 9.01028 2.89016C9.08061 2.81984 9.12012 2.72446 9.12012 2.625V0.375C9.12012 0.275544 9.08061 0.180161 9.01028 0.109835C8.93996 0.0395088 8.84457 0 8.74512 0C8.64566 0 8.55028 0.0395088 8.47995 0.109835C8.40963 0.180161 8.37012 0.275544 8.37012 0.375V2.625C8.37012 2.72446 8.40963 2.81984 8.47995 2.89016C8.55028 2.96049 8.64566 3 8.74512 3Z"
                fill="#4F4F4F"
              />
              <path
                d="M7.24512 2.99998C7.34457 2.99998 7.43996 2.96047 7.51028 2.89014C7.58061 2.81982 7.62012 2.72443 7.62012 2.62498V0.631103C7.62012 0.531647 7.58061 0.436265 7.51028 0.365938C7.43996 0.295612 7.34457 0.256104 7.24512 0.256104C7.14566 0.256104 7.05028 0.295612 6.97995 0.365938C6.90962 0.436265 6.87012 0.531647 6.87012 0.631103V2.62498C6.87012 2.72443 6.90962 2.81982 6.97995 2.89014C7.05028 2.96047 7.14566 2.99998 7.24512 2.99998Z"
                fill="#4F4F4F"
              />
              <path
                d="M10.2451 2.99998C10.3446 2.99998 10.44 2.96047 10.5103 2.89014C10.5806 2.81982 10.6201 2.72443 10.6201 2.62498V0.631103C10.6201 0.531647 10.5806 0.436265 10.5103 0.365938C10.44 0.295612 10.3446 0.256104 10.2451 0.256104C10.1457 0.256104 10.0503 0.295612 9.97995 0.365938C9.90963 0.436265 9.87012 0.531647 9.87012 0.631103V2.62498C9.87012 2.72443 9.90963 2.81982 9.97995 2.89014C10.0503 2.96047 10.1457 2.99998 10.2451 2.99998Z"
                fill="#4F4F4F"
              />
              <path d="M14.7451 9H2.74512V9.75H14.7451V9Z" fill="#4F4F4F" />
              <path
                d="M10.2451 5.25H13.2451C13.3446 5.25 13.44 5.21049 13.5103 5.14016C13.5806 5.06984 13.6201 4.97446 13.6201 4.875C13.6201 4.77554 13.5806 4.68016 13.5103 4.60984C13.44 4.53951 13.3446 4.5 13.2451 4.5H10.2451C10.1457 4.5 10.0503 4.53951 9.97995 4.60984C9.90963 4.68016 9.87012 4.77554 9.87012 4.875C9.87012 4.97446 9.90963 5.06984 9.97995 5.14016C10.0503 5.21049 10.1457 5.25 10.2451 5.25Z"
                fill="#4F4F4F"
              />
              <path
                d="M10.2451 6.75H13.2451C13.3446 6.75 13.44 6.71049 13.5103 6.64017C13.5806 6.56984 13.6201 6.47446 13.6201 6.375C13.6201 6.27554 13.5806 6.18016 13.5103 6.10983C13.44 6.03951 13.3446 6 13.2451 6H10.2451C10.1457 6 10.0503 6.03951 9.97995 6.10983C9.90963 6.18016 9.87012 6.27554 9.87012 6.375C9.87012 6.47446 9.90963 6.56984 9.97995 6.64017C10.0503 6.71049 10.1457 6.75 10.2451 6.75Z"
                fill="#4F4F4F"
              />
              <path
                d="M4.24512 5.25H7.24512C7.34457 5.25 7.43996 5.21049 7.51028 5.14016C7.58061 5.06984 7.62012 4.97446 7.62012 4.875C7.62012 4.77554 7.58061 4.68016 7.51028 4.60984C7.43996 4.53951 7.34457 4.5 7.24512 4.5H4.24512C4.14566 4.5 4.05028 4.53951 3.97995 4.60984C3.90963 4.68016 3.87012 4.77554 3.87012 4.875C3.87012 4.97446 3.90963 5.06984 3.97995 5.14016C4.05028 5.21049 4.14566 5.25 4.24512 5.25Z"
                fill="#4F4F4F"
              />
              <path
                d="M4.24512 6.75H7.24512C7.34457 6.75 7.43996 6.71049 7.51028 6.64017C7.58061 6.56984 7.62012 6.47446 7.62012 6.375C7.62012 6.27554 7.58061 6.18016 7.51028 6.10983C7.43996 6.03951 7.34457 6 7.24512 6H4.24512C4.14566 6 4.05028 6.03951 3.97995 6.10983C3.90963 6.18016 3.87012 6.27554 3.87012 6.375C3.87012 6.47446 3.90963 6.56984 3.97995 6.64017C4.05028 6.71049 4.14566 6.75 4.24512 6.75Z"
                fill="#4F4F4F"
              />
              <path
                d="M10.2451 8.25H13.2451C13.3446 8.25 13.44 8.21049 13.5103 8.14016C13.5806 8.06984 13.6201 7.97446 13.6201 7.875C13.6201 7.77554 13.5806 7.68016 13.5103 7.60983C13.44 7.53951 13.3446 7.5 13.2451 7.5H10.2451C10.1457 7.5 10.0503 7.53951 9.97995 7.60983C9.90963 7.68016 9.87012 7.77554 9.87012 7.875C9.87012 7.97446 9.90963 8.06984 9.97995 8.14016C10.0503 8.21049 10.1457 8.25 10.2451 8.25Z"
                fill="#4F4F4F"
              />
              <path
                d="M4.24512 8.25H7.24512C7.34457 8.25 7.43996 8.21049 7.51028 8.14016C7.58061 8.06984 7.62012 7.97446 7.62012 7.875C7.62012 7.77554 7.58061 7.68016 7.51028 7.60983C7.43996 7.53951 7.34457 7.5 7.24512 7.5H4.24512C4.14566 7.5 4.05028 7.53951 3.97995 7.60983C3.90963 7.68016 3.87012 7.77554 3.87012 7.875C3.87012 7.97446 3.90963 8.06984 3.97995 8.14016C4.05028 8.21049 4.14566 8.25 4.24512 8.25Z"
                fill="#4F4F4F"
              />
              <line x1="16.386" y1="1.31785" x2="2.38597" y2="18.3179" stroke="#4F4F4F" />
            </g>
            <defs>
              <clipPath id="clip0">
                <rect width="18" height="18" transform="matrix(-1 0 0 1 18 0)" fill="white" />
              </clipPath>
            </defs>
          </svg>
        </li>
        <li>
          <svg
            width="18"
            height="18"
            viewBox="0 0 18 18"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M8.25 18H9.75C10.3703 18 10.875 17.4953 10.875 16.875V15.4785C11.3551 15.3397 11.8181 15.1477 12.2554 14.9059L13.2431 15.894C13.6684 16.3193 14.409 16.3185 14.8342 15.894L15.8951 14.8335C16.1078 14.6213 16.2247 14.3385 16.2247 14.0381C16.2247 13.7378 16.1078 13.455 15.8951 13.2428L14.907 12.2543C15.1488 11.8173 15.3406 11.3545 15.4789 10.8746H16.875C17.4952 10.8746 18 10.3699 18 9.74963V8.24963C18 7.94888 17.883 7.6665 17.6707 7.45425C17.5665 7.34947 17.4424 7.26638 17.3059 7.20981C17.1693 7.15323 17.0228 7.12428 16.875 7.12463H15.4785C15.3398 6.64538 15.1485 6.183 14.9062 5.745L15.894 4.75688C16.1047 4.54581 16.2231 4.25975 16.2231 3.9615C16.2231 3.66325 16.1047 3.37719 15.894 3.16612L14.8335 2.10525C14.4086 1.68075 13.6676 1.68 13.2424 2.10525L12.2543 3.09337C11.8173 2.85189 11.3546 2.66007 10.875 2.5215V1.125C10.875 0.50475 10.3703 0 9.75 0H8.25C7.62975 0 7.125 0.50475 7.125 1.125V2.5215C6.645 2.66025 6.183 2.85187 5.74575 3.09337L4.75763 2.10525C4.33238 1.68075 3.59175 1.68 3.1665 2.10525L2.10563 3.16575C1.893 3.378 1.776 3.66075 1.776 3.96112C1.776 4.2615 1.893 4.54425 2.10563 4.7565L3.09338 5.74463C2.85148 6.18171 2.65952 6.64462 2.52112 7.12463H1.125C0.504749 7.12463 0 7.62937 0 8.24963V9.74963C0 10.0504 0.116999 10.3328 0.32925 10.545C0.5415 10.7572 0.824249 10.8746 1.125 10.8746H2.5215C2.66016 11.3545 2.8521 11.8174 3.09375 12.2546L2.106 13.2428C1.89528 13.4538 1.77693 13.7399 1.77693 14.0381C1.77693 14.3364 1.89528 14.6224 2.106 14.8335L3.1665 15.8944C3.59175 16.3193 4.33238 16.3193 4.75763 15.8944L5.745 14.9062C6.18209 15.1479 6.64485 15.3398 7.12463 15.4785V16.875C7.12512 17.1733 7.24386 17.4592 7.45481 17.6701C7.66576 17.881 7.95172 17.9996 8.25 18ZM12.3161 14.0618C12.249 14.0618 12.1811 14.0798 12.1207 14.1165C11.5916 14.4405 11.015 14.6797 10.4119 14.8256C10.3301 14.8454 10.2574 14.8921 10.2053 14.9582C10.1533 15.0243 10.125 15.106 10.125 15.1901V16.875C10.125 17.082 9.95662 17.25 9.75 17.25H8.25C8.04338 17.25 7.875 17.082 7.875 16.875V15.1901C7.875 15.106 7.84671 15.0243 7.79468 14.9582C7.74265 14.8921 7.6699 14.8454 7.58813 14.8256C6.98518 14.6798 6.40872 14.4407 5.87963 14.1169C5.73112 14.0265 5.54138 14.0494 5.41875 14.1716L4.227 15.3638C4.08637 15.504 3.83737 15.5048 3.69637 15.3638L2.63587 14.3029C2.56557 14.2326 2.52608 14.1372 2.52608 14.0377C2.52608 13.9383 2.56557 13.8429 2.63587 13.7726L3.828 12.5805C3.88753 12.521 3.92531 12.4432 3.93524 12.3596C3.94517 12.276 3.92668 12.1914 3.88275 12.1196C3.55898 11.5905 3.31996 11.0141 3.17438 10.4111C3.15468 10.3293 3.10801 10.2564 3.0419 10.2043C2.97578 10.1522 2.89406 10.1239 2.80988 10.1239H1.125C1.07576 10.1241 1.02697 10.1145 0.981434 10.0958C0.935896 10.0771 0.89451 10.0495 0.859659 10.0147C0.824806 9.97997 0.797176 9.93863 0.778357 9.89314C0.759537 9.84764 0.749901 9.79886 0.75 9.74963V8.24963C0.75 8.04263 0.918375 7.87463 1.125 7.87463H2.80988C2.89407 7.87467 2.97583 7.84635 3.04196 7.79424C3.10809 7.74212 3.15474 7.66925 3.17438 7.58737C3.3199 6.9844 3.55892 6.40792 3.88275 5.87887C3.92668 5.80706 3.94517 5.72255 3.93524 5.63895C3.92531 5.55535 3.88753 5.47752 3.828 5.418L2.63587 4.22587C2.56612 4.15575 2.526 4.05938 2.526 3.96075C2.526 3.86213 2.56612 3.76537 2.63587 3.69562L3.69675 2.63512C3.76833 2.56709 3.86331 2.52916 3.96206 2.52916C4.06081 2.52916 4.15579 2.56709 4.22738 2.63512L5.4195 3.82725C5.47885 3.88708 5.5567 3.92506 5.64039 3.935C5.72407 3.94494 5.80866 3.92626 5.88037 3.882C6.40923 3.55832 6.98544 3.31931 7.58813 3.17362C7.66987 3.15407 7.74264 3.10753 7.79469 3.04154C7.84674 2.97554 7.87503 2.89393 7.875 2.80988V1.125C7.875 0.918 8.04338 0.75 8.25 0.75H9.75C9.95662 0.75 10.125 0.918 10.125 1.125V2.80988C10.125 2.894 10.1533 2.97569 10.2053 3.0418C10.2574 3.10791 10.3301 3.1546 10.4119 3.17438C11.0148 3.32004 11.5913 3.55905 12.1204 3.88275C12.1921 3.92672 12.2766 3.94523 12.3601 3.9353C12.4437 3.92536 12.5214 3.88756 12.5809 3.828L13.773 2.63587C13.8446 2.56784 13.9396 2.52991 14.0383 2.52991C14.1371 2.52991 14.232 2.56784 14.3036 2.63587L15.3637 3.69638C15.4341 3.7667 15.4735 3.86206 15.4735 3.9615C15.4735 4.06094 15.4341 4.1563 15.3637 4.22662L14.1716 5.41875C14.1121 5.47827 14.0743 5.5561 14.0644 5.6397C14.0545 5.7233 14.0729 5.80781 14.1169 5.87962C14.4406 6.40857 14.6796 6.98492 14.8253 7.58775C14.8449 7.66959 14.8916 7.74243 14.9577 7.79453C15.0238 7.84664 15.1056 7.87498 15.1897 7.875H16.875C16.9243 7.8748 16.9731 7.88435 17.0187 7.90311C17.0642 7.92186 17.1056 7.94944 17.1405 7.98426C17.1753 8.01908 17.203 8.06046 17.2218 8.106C17.2405 8.15154 17.2501 8.20036 17.25 8.24963V9.74963C17.25 9.95662 17.0816 10.1246 16.875 10.1246H15.1901C15.0169 10.1246 14.8661 10.2431 14.8256 10.4119C14.68 11.0147 14.441 11.591 14.1172 12.12C14.0733 12.1918 14.0548 12.2763 14.0648 12.3599C14.0747 12.4435 14.1125 12.5214 14.172 12.5809L15.3641 13.7734C15.4339 13.8435 15.474 13.9399 15.474 14.0385C15.474 14.1371 15.4339 14.2339 15.3641 14.3036L14.3033 15.3641C14.2317 15.4322 14.1367 15.4701 14.0379 15.4701C13.9392 15.4701 13.8442 15.4322 13.7726 15.3641L12.5809 14.172C12.5463 14.137 12.505 14.1092 12.4596 14.0903C12.4141 14.0714 12.3654 14.0617 12.3161 14.0618Z"
              fill="#4F4F4F"
            />
            <path
              d="M9 12.75C11.0677 12.75 12.75 11.0677 12.75 9C12.75 6.93225 11.0677 5.25 9 5.25C6.93225 5.25 5.25 6.93225 5.25 9C5.25 11.0677 6.93187 12.75 9 12.75ZM9 6C10.6541 6 12 7.34587 12 9C12 10.6541 10.6541 12 9 12C7.34587 12 6 10.6541 6 9C6 7.34587 7.3455 6 9 6Z"
              fill="#4F4F4F"
            />
          </svg>
        </li>
      </ul>
    </div>
    <div>
      <div :class="['dropdown', {'is-active' : stateMenuIsActive}]">
        <div class="dropdown-trigger">
          <button
            @click="stateMenuIsActive = !stateMenuIsActive"
            class="button"
            aria-haspopup="true"
            aria-controls="dropdown-menu2"
          >
            <span>{{userState}}</span>
            <span class="icon is-small">
              <font-awesome-icon icon="angle-down" />
            </span>
          </button>
        </div>
        <div class="dropdown-menu" id="dropdown-menu2" role="menu">
          <div class="dropdown-content">
            <div v-for="(state, index) in states" :key="state" @click="handleState(state)">
              <div class="dropdown-item">{{state}}</div>
              <hr v-if="index + 1 !== states.length" class="dropdown-divider" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import Avatar from "@/components/Avatar";
export default {
  name: "UserCard",
  props: {
    float: {
      type: Boolean
    },
    sound: {
      type: Boolean
    },
    micro: {
      type: Boolean
    },
    user: {
      type: Object
    }
  },
  components: {
    Avatar
  },
  data() {
    return {
      stateMenuIsActive: false,
      states: [
        "💻 Disponible",
        " 🤝En reunión",
        "😋 En colación",
        "👻 Ausente"
      ],
      userState: null
    };
  },
  created () {
    this.userState = this.states[0]
  },
  methods: {
    emitSound() {
      this.$emit("sound");
    },
    emitMicro() {
      this.$emit("micro");
    },
    handleState(state) {
      this.userState = state;
      this.stateMenuIsActive = false;
    }
  }
};
</script>
<style lang="scss" scoped>
.connect-user-card {
  position: fixed;
  top: 7px;
  right: 8px;
  width: 326px;
  padding: 15px 8px 15px;
  transition: $aside-transition;
  transition-delay: 0.25s;
  background-color: #fff;

  > div {
    display: inline-flex;
    width: 100%;
    justify-content: space-between;
  }

  &-info {
    display: flex;
    align-items: center;
    justify-content: space-between;

    &-text {
      margin-left: 10px;
      h3 {
        font-size: 16px;
      }

      p {
        font-size: 12px;
      }
    }
  }

  &-options {
    display: inline-flex;

    li {
      margin-left: 10px;
      cursor: pointer;
    }
  }

  &--floats {
    box-shadow: $card-box-shadow;
    background: #fff;
    border-radius: $card-border-radius;
  }
}

.dropdown {
  width: 100%;

  &-trigger {
    width: 100%;
  }

  button {
    width: 100%;
    display: flex;
    justify-content: space-between;
  }

  &.is-active {
    .dropdown-menu {
      width: 100%;

      .dropdown-item {
        &:hover {
          background: $light-gray;
          cursor: pointer;
        }
      }
    }
  }
}

.button {
  margin-top: 5px;
  background-color: $light-gray;
  border: 0;
  padding: 3px 10px;
  text-align: center;
  white-space: nowrap;
  height: 30px;
}
</style>