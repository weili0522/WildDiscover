export default function middleware(req) {
  const url = new URL(req.url)
  
  // Skip API routes or static assets if necessary
  if (url.pathname.startsWith('/api') || url.pathname.includes('.')) {
    return
  }

  const authHeader = req.headers.get('authorization')
  
  const expectedUser = process.env.AUTH_USER
  const expectedPassword = process.env.AUTH_PASSWORD

  if (authHeader) {
    try {
      const authValue = authHeader.split(' ')[1]
      const decoded = atob(authValue)
      const [user, pwd] = decoded.split(':')

      if (user === expectedUser && pwd === expectedPassword) {
        return // Let the request pass through
      }
    } catch (e) {
      // Malformed auth header, fall through to 401
    }
  }

  return new Response('Auth required.', {
    status: 401,
    headers: {
      'WWW-Authenticate': 'Basic realm="Secure Area"',
    },
  })
}
