FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json and install dependencies
COPY package.json tsconfig.json ./
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the React app
RUN npm run build

# Use a lightweight web server to serve the built app
FROM nginx:1.23-alpine AS production

# Copy the build output to the Nginx HTML directory
COPY --from=0 /app/build /usr/share/nginx/html

# Expose port 80 for the frontend
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]