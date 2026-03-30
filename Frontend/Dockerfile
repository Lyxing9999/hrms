FROM node:22-alpine

WORKDIR /app

RUN npm install -g pnpm

COPY package.json pnpm-lock.yaml* ./
RUN pnpm install --no-frozen-lockfile

COPY . .

EXPOSE 3000

CMD ["sh", "-lc", "pnpm install --no-frozen-lockfile && pnpm dev --host 0.0.0.0 --port 3000"]