# Use an official Node runtime as a parent image
FROM node:alpine

ARG NEXT_PUBLIC_API_URL='http://override-me-in-docker-compose'
ENV NEXT_PUBLIC_API_URL $NEXT_PUBLIC_API_URL

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json (or yarn.lock)
COPY app/package*.json ./

# Install dependencies
RUN npm install

# Bundle app source inside Docker image
COPY app/. .

# Build the Next.js app
RUN npm run build

# Define the command to run your app
CMD [ "npm", "start" ]
