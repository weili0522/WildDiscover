import { NextResponse } from 'next/server'

export function middleware(req) {
  const basicAuth = req.headers.get('authorization')

  const expectedUser = process.env.AUTH_USER
  const expectedPassword = process.env.AUTH_PASSWORD

  if (basicAuth) {
    const authValue = basicAuth.split(' ')[1]
    const [user, pwd] = atob(authValue).split(':')

    if (user === expectedUser && pwd === expectedPassword) {
      return NextResponse.next()
    }
  }

  return new NextResponse('Auth required.', {
    status: 401,
    headers: {
      'WWW-Authenticate': 'Basic realm="Secure Area"',
    },
  })
}

export const config = {
  matcher: '/((?!api|_next/static|_next/image|favicon.ico).*)',
}
