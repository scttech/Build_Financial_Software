import type { NextAuthConfig } from 'next-auth';

export const authConfig = {
    debug: true,
    pages: {
        signIn: '/login',
    },
    callbacks: {
        authorized({ auth, request: { nextUrl } }) {
            const isLoggedIn = !!auth?.user;
            const isOnDashboard = nextUrl.pathname.startsWith('/uploads');
            if (isOnDashboard) {
                return isLoggedIn;
            } else if (isLoggedIn) {
                return Response.redirect(new URL('/login', nextUrl));
            }
            return true;
        },
        async redirect({ url, baseUrl }) {
            const queryParams = new URL(url).searchParams;
            const callbackUrl = queryParams.get('callbackUrl');
            if (callbackUrl) {
                return callbackUrl;
            } else {
                return url.startsWith(baseUrl) ? url : baseUrl;
            }
        }
    },
    providers: [],
} satisfies NextAuthConfig;