# Étape 1 : Construire l'application
FROM node:18 AS build

WORKDIR /app

# Copier les fichiers de l'application
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Étape 2 : Servir l'application construite
FROM nginx:alpine

COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
