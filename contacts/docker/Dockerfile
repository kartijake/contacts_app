# Step 1: Build Vite React App
FROM node:22 AS build

WORKDIR /app

# Copy package.json and install dependencies
COPY ../package.json ../package-lock.json ./
RUN npm install --frozen-lockfile

# Copy all project files (excluding Docker stuff)
COPY ../ ./

# Build the React app
RUN npm run build

# Step 2: Serve React App with Nginx
FROM nginx:latest

# Copy built files from build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Ensure nginx.conf exists in /docker and copy it correctly
COPY ../docker/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 5000
EXPOSE 5000

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
