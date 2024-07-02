import NextAuth from 'next-auth';
import Credentials from 'next-auth/providers/credentials';
import { z } from 'zod';
import { authConfig } from './auth.config';

const validUsers = [
    { email: 'admin@futuristicfintech.com', password: 'password'},
    { email: 'user@futuristicfintech.com', password: 'password'}
    ]

export const { auth, signIn, signOut } = NextAuth({
    ...authConfig,
    providers: [
        Credentials({
            async authorize(credentials) {
                const parsedCredentials = z.object({
                    email: z.string(),
                    password: z.string(),
                }).safeParse(credentials);

                if (!parsedCredentials.success) {
                    return null;
                }

                const { email, password } = parsedCredentials.data;

                // Validate against hardcoded list
                const user = validUsers.find(user => user.email === email && user.password === password);

                if (!user) {
                    return null;
                }

                return { email: user.email };
            },
        }),
    ],
});