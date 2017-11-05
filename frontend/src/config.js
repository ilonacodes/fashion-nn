export const config = {
  apiGateway: process.env.NODE_ENV === 'production' ? '' : 'http://localhost:8080',
}
