> DEVELOPER

{ level: 'log', pid: 57625, timestamp: 1776372927726, correlationId: '04d94fef-85b7-4dd0-9e15-fd31c7d47c2b', message: { namespace: 'github-token', key: '124532566' }, context: 'CacheService' }
{ level: 'debug', pid: 57625, timestamp: 1776372928167, correlationId: '19823d48-ecbf-45c5-84d9-52fc3d89d4a5', message: 'Upserted 97 commits', context: 'GithubCommitModel' }
{ level: 'debug', pid: 57625, timestamp: 1776372928167, correlationId: '329f95ca-ecc7-4162-a3fe-ba00c1e701b2', message: 'Backfilled commits for no-name-proj-dev-test/api-service', context: 'GithubEventProcessor' }
{ level: 'debug', pid: 57625, timestamp: 1776372928466, correlationId: 'a1cd5d8a-bce4-4343-be62-5dc31bb7b83c', message: 'Upserted contributor 4thwithme for installation 4ac7754e-1cd5-4eba-8793-6347da70979c', context: 'GithubContributorModel' }
{ level: 'debug', pid: 57625, timestamp: 1776372928469, correlationId: '0e5a9dab-596f-4e77-a906-cd63a8ef42d2', message: 'Upserted pull request #3 for repo 51af1985-3d56-4b60-b14f-aeedb749e5f8', context: 'GithubPullRequestModel' }
{ level: 'debug', pid: 57625, timestamp: 1776372928885, correlationId: '3359fa39-90c9-48ca-a76c-ef5866834d30', message: 'Upserted contributor 4thwithme for installation 4ac7754e-1cd5-4eba-8793-6347da70979c', context: 'GithubContributorModel' }
{ level: 'debug', pid: 57625, timestamp: 1776372928889, correlationId: '152dbe95-aca3-45b9-8597-d70ff77eee78', message: 'Upserted review 4123170065 for pull request dd2610ea-5bcf-4338-9c38-f997aa03fd45', context: 'GithubReviewModel' }
{ level: 'debug', pid: 57625, timestamp: 1776372929159, correlationId: '0d067523-530c-407f-95a6-435630e511b1', message: 'Upserted contributor 4thwithme for installation 4ac7754e-1cd5-4eba-8793-6347da70979c', context: 'GithubContributorModel' }
{ level: 'debug', pid: 57625, timestamp: 1776372929163, correlationId: '8dac488e-cd8e-4eb2-a937-b64e498be192', message: 'Upserted pull request #2 for repo 51af1985-3d56-4b60-b14f-aeedb749e5f8', context: 'GithubPullRequestModel' }
{ level: 'debug', pid: 57625, timestamp: 1776372929689, correlationId: '56810025-6dba-42c1-9917-907a9c6d91b7', message: 'Upserted contributor 4thwithme for installation 4ac7754e-1cd5-4eba-8793-6347da70979c', context: 'GithubContributorModel' }
{ level: 'debug', pid: 57625, timestamp: 1776372929693, correlationId: '9d109377-a3e7-45e9-85bf-b27a23b6f8e5', message: 'Upserted pull […]

> AGENT

Yes. Clean backfill for both repos — commits, PRs, reviews, contributors all upserted. No errors.

> DEVELOPER

ok seems like it works for dev

> AGENT

Good. Ready to move to the next phase?

> TOOL

tool_use Write
id: toolu_01GLTXALZ9gfE821b3SaWpM6
```json
{
  "file_path": "/home/<USER>/.claude/projects/-Users-4thwithme-Documents-repo-no-name-proj/memory/project_github_ingestion.md",
  "content": "---\nname: GitHub data ingestion status\ndescription: Status of GitHub Phase 2 data ingestion pipeline\ntype: project\n---\n\nGitHub backfill pipeline (commits, PRs, reviews, contributors) working in dev as of 2026-04-16.\n\n**Why:** Validated via manual test against no-name-proj-dev-test org (api-service + frontend-app repos).\n\n**How to apply:** Dev environment is confirmed working — next step is likely staging/prod validation or moving to next roadmap phase.\n"
}
```

> TOOL

tool_result
id: toolu_01GLTXALZ9gfE821b3SaWpM6
```
File created successfully at: /home/<USER>/.claude/projects/-Users-4thwithme-Documents-repo-no-name-proj/memory/project_github_ingestion.md
```

> DEVELOPER

how to test it manually for JIRA integration?

> AGENT

Let me check the Jira controller and install flow.

> TOOL

tool_use Read
id: toolu_018ysmE9Fm9geFBUk77gTTki
```json
{
  "file_path": "/home/<USER>/Documents/repo/no-name-proj/backend/src/modules/jira/jira.controller.ts"
}
```

> TOOL

tool_result
id: toolu_018ysmE9Fm9geFBUk77gTTki
```
1	import {
2		Controller,
3		Delete,
4		Get,
5		HttpCode,
6		HttpStatus,
7		Param,
8		Post,
9		Query,
10		Res,
11	} from '@nestjs/common';
12	import { ApiOperation, ApiResponse, ApiTags } from '@nestjs/swagger';
13	
14	import { CurrentUser } from '@modules/auth/decorators/current-user.decorator';
15	import { Roles } from '@modules/auth/decorators/roles.decorator';
16	import { IRequestUser } from '@modules/auth/types/auth.interface';
17	import { EnvConfigService } from '@modules/env-config/env-config.service';
18	import { JiraInstallService } from '@modules/jira/jira-install.service';
19	
20	import { FRONTEND_URL } from '@constants/env-variables.constant';
21	
22	import { LogExecution } from '@decorators/log-execution.decorator';
23	
24	import type { FastifyReply } from 'fastify';
25	
26	@ApiTags('Jira Integration')
27	@Controller('integrations/jira')
28	export class JiraController {
29		constructor(
30			private readonly jiraInstallService: JiraInstallService,
31			private readonly configService: EnvConfigService,
32		) {}
33	
34		@Post('connect')
35		@Roles('admin')
36		@HttpCode(HttpStatus.OK)
37		@ApiOperation({ summary: 'Initiate Jira OAuth connection' })
38		@ApiResponse({ status: HttpStatus.OK, description: 'Returns Atlassian OAuth URL' })
39		@LogExecution()
40		async connect(@CurrentUser() user: IRequestUser): Promise<{ url: string }> {
41			// eslint-disable-next-line @typescript-eslint/no-non-null-assertion
42			const companyId = user.company_id!;
43			const url = await this.jiraInstallService.initiateConnect({
44				companyId,
45				userId: user.user_id,
46			});
47			return { url };
48		}
49	
50		@Get('callback')
51		@Roles('admin')
52		@HttpCode(HttpStatus.FOUND)
53		@ApiOperation({ […]

> AGENT

The Jira flow is OAuth-based. Manual testing steps:

1. **Trigger connect** (need auth token with admin role):
```bash
curl -X POST http://localhost:3000/integrations/jira/connect \
  -H "Authorization: Bearer <your-jwt>" \
  -H "Content-Type: application/json"
```
Returns `{ url: "https://auth.atlassian.com/..." }`

2. **Open that URL** in browser → authorize the app on Atlassian

3. **Atlassian redirects** to `GET /integrations/jira/callback?code=...&state=...` — handled automatically

4. **Check logs** — should see installation upserted (similar to GitHub backfill logs)

5. **Disconnect** to clean up:
```bash
curl -X DELETE http://localhost:3000/integrations/jira/installations/<id> \
  -H "Authorization: Bearer <your-jwt>"
```

Do you have a dev Atlassian account/org to test against, or need help getting a test JWT?

> DEVELOPER

give me all curl as 1 liners

> AGENT

```bash
curl -s -X POST http://localhost:3000/integrations/jira/connect -H "Authorization: Bearer <your-jwt>" -H "Content-Type: application/json"
```

```bash
curl -s -X DELETE http://localhost:3000/integrations/jira/installations/<id> -H "Authorization: Bearer <your-jwt>"
```

Step 2 (open OAuth URL) and step 3 (callback) can't be curled — need a browser for the Atlassian OAuth flow.

> DEVELOPER

where to get token?

> AGENT

Let me check the auth module.

> TOOL

tool_use Glob
id: toolu_01QFYHL31iLB264wJRW1zV22
```json
{
  "pattern": "backend/src/modules/auth/**/*.ts"
}
```

> TOOL

tool_result
id: toolu_01QFYHL31iLB264wJRW1zV22
```
backend/src/modules/auth/types/auth.interface.ts
backend/src/modules/auth/decorators/current-user.decorator.ts
backend/src/modules/auth/decorators/public.decorator.ts
backend/src/modules/auth/decorators/roles.decorator.ts
backend/src/modules/auth/dto/token-exchange.dto.ts
backend/src/modules/auth/dto/link-account.dto.ts
backend/src/modules/auth/dto/create-company.dto.ts
backend/src/modules/auth/auth.module.ts
backend/src/modules/auth/strategies/github.strategy.ts
backend/src/modules/auth/strategies/google.strategy.ts
backend/src/modules/auth/auth.service.ts
backend/src/modules/auth/guards/roles.guard.ts
backend/src/modules/auth/guards/auth.guard.ts
backend/src/modules/auth/guards/fastify-throttler.guard.ts
backend/src/modules/auth/constants/auth.constant.ts
backend/src/modules/auth/guards/csrf.guard.ts
backend/src/modules/auth/auth.controller.ts
```

> TOOL

tool_use Read
id: toolu_014rNDWbDQp3UkDSt8ZVxRBc
```json
{
  "file_path": "/home/<USER>/Documents/repo/no-name-proj/backend/src/modules/auth/auth.controller.ts"
}
```

> TOOL

tool_result
id: toolu_014rNDWbDQp3UkDSt8ZVxRBc
```
1	import '@fastify/cookie';
2	
3	import { randomBytes } from 'node:crypto';
4	
5	import {
6		Body,
7		Controller,
8		Get,
9		HttpStatus,
10		Post,
11		Query,
12		Req,
13		Res,
14		UnauthorizedException,
15		UseGuards,
16	} from '@nestjs/common';
17	import { ApiOperation, ApiResponse, ApiTags } from '@nestjs/swagger';
18	import { Throttle } from '@nestjs/throttler';
19	import { FastifyReply, FastifyRequest } from 'fastify';
20	
21	import { AuthService } from '@modules/auth/auth.service';
22	import {
23		CSRF_TOKEN_COOKIE_NAME,
24		REFRESH_TOKEN_COOKIE_NAME,
25	} from '@modules/auth/constants/auth.constant';
26	import { CurrentUser } from '@modules/auth/decorators/current-user.decorator';
27	import { Public } from '@modules/auth/decorators/public.decorator';
28	import { CreateCompanyDto } from '@modules/auth/dto/create-company.dto';
29	import { LinkAccountDto } from '@modules/auth/dto/link-account.dto';
30	import { TokenExchangeDto } from '@modules/auth/dto/token-exchange.dto';
31	import { CsrfGuard } from '@modules/auth/guards/csrf.guard';
32	import { IRequestUser } from '@modules/auth/types/auth.interface';
33	
34	import { isDevEnv } from '@utils/common.util';
35	import { getEnv } from '@utils/get-env-variable.util';
36	
37	import { FRONTEND_URL } from '@constants/env-variables.constant';
38	
39	import { LogExecution } from '@decorators/log-execution.decorator';
40	
41	@ApiTags('Auth')
42	@Throttle({ default: { limit: 10, ttl: 60000 } })
43	@Controller('auth')
44	export class AuthController {
45		constructor(private readonly authService: AuthService) {}
46	
47		private setCsrfCookie({ reply }: { reply: […]

> AGENT

OAuth-only — no username/password. Full flow:

**Step 1:** Open in browser (can't curl — needs redirect):
```
http://localhost:3000/auth/github
```

**Step 2:** After GitHub OAuth, you'll be redirected to frontend with `?code=XXX`. Grab that code from the URL.

**Step 3:** Exchange for JWT:
```bash
curl -s -X POST http://localhost:3000/auth/token -H "Content-Type: application/json" -d '{"code":"<code-from-url>"}'
```

Returns `{ "access_token": "eyJ..." }` — use that as your Bearer token.

> DEVELOPER

why github if i need to tesj jira?

> AGENT

The JWT is for **our API**, not Jira. You log into our app via GitHub/Google OAuth — the resulting token authenticates you to all endpoints, including `POST /integrations/jira/connect`. GitHub here = your login method, not Jira access.

> DEVELOPER

http://localhost:3000/auth/github this is wrongg link

> TOOL

tool_use Read
id: toolu_01BmWSx1pCrRzejSnAUcnrhX
```json
{
  "file_path": "/home/<USER>/Documents/repo/no-name-proj/backend/src/main.ts"
}
```

> TOOL

tool_result
id: toolu_01BmWSx1pCrRzejSnAUcnrhX
```
1	import { PassThrough } from 'node:stream';
2	
3	import fastifyCookie from '@fastify/cookie';
4	import { Logger, ValidationPipe } from '@nestjs/common';
5	import { NestFactory } from '@nestjs/core';
6	import { FastifyAdapter, NestFastifyApplication } from '@nestjs/platform-fastify';
7	
8	import { AppConsoleLogger } from '@config/custom-logger.config';
9	
10	import { AppModule } from '@modules/app/app.module';
11	
12	import { getEnv } from '@utils/get-env-variable.util';
13	import { setupSwagger } from '@utils/setup-swagger.util';
14	
15	import { fastifyHttpLogger } from '@middlewares/logger.middleware';
16	
17	import {
18		FRONTEND_URL,
19		GLOBAL_PREFIX,
20		IS_COMPACT_LOGS,
21		IS_JSON_LIKE_LOGS,
22		NODE_ENV,
23		PORT,
24		SERVER_NAME,
25	} from '@constants/env-variables.constant';
26	
27	import { Environment } from '@interfaces/env-variables.interface';
28	
29	declare const module: {
30		hot?: { accept: () => void; dispose: (callback: () => void) => void };
31	};
32	
33	async function bootstrap(): Promise<NestFastifyApplication> {
34		const port = getEnv<number>({ key: PORT, converter: Number });
35		const globalPrefix = getEnv<string>({ key: GLOBAL_PREFIX });
36		const nodeEnv = getEnv<Environment>({ key: NODE_ENV });
37		const isDev = nodeEnv === Environment.DEVELOPMENT;
38		const serverName = getEnv<string>({ key: SERVER_NAME });
39		const isCompactLogs = getEnv<boolean>({ key: IS_COMPACT_LOGS, converter: Boolean });
40		const isJsonLikeLogs = getEnv<boolean>({ key: IS_JSON_LIKE_LOGS, converter: Boolean }); […]

> AGENT

There's a global prefix. Let me check what it is.

> TOOL

tool_use Grep
id: toolu_015HBCWXpRzebvDUbaQDQXL9
```json
{
  "pattern": "GLOBAL_PREFIX",
  "path": "backend/.env.example",
  "output_mode": "content"
}
```

> TOOL

tool_result
id: toolu_015HBCWXpRzebvDUbaQDQXL9
```
3:GLOBAL_PREFIX=api
```

> TOOL

tool_use Grep
id: toolu_01MifEjhY6EqV1dfGJtCGJev
```json
{
  "pattern": "^PORT=",
  "path": "backend/.env.example",
  "output_mode": "content"
}
```

> TOOL

tool_result
id: toolu_01MifEjhY6EqV1dfGJtCGJev
```
2:PORT=9069
```

> AGENT

Correct URL:
```
http://localhost:9069/api/auth/github
```

And all curl commands update accordingly:
```bash
curl -s -X POST http://localhost:9069/api/auth/token -H "Content-Type: application/json" -d '{"code":"<code-from-url>"}'
```
```bash
curl -s -X POST http://localhost:9069/api/integrations/jira/connect -H "Authorization: Bearer <token>" -H "Content-Type: application/json"
```
```bash
curl -s -X DELETE http://localhost:9069/api/integrations/jira/installations/<id> -H "Authorization: Bearer <token>"
```

> DEVELOPER

curl -s -X POST http://localhost:9069/api/integrations/jira/connect -H "Authorization: bearer [REDACTED]" -H "Content-Type: application/json"
{"statusCode":400,"message":"Body cannot be empty when content-type is set to 'application/json'"}%

> AGENT

Drop the `Content-Type` header — no body needed:

```bash
curl -s -X POST http://localhost:9069/api/integrations/jira/connect -H "Authorization: bearer [REDACTED]"
```

> DEVELOPER

curl -s -X POST http://localhost:9069/api/integrations/jira/connect -H "Authorization: bearer [REDACTED]"
{"message":"Unauthorized","statusCode":401}%

> AGENT

That's not a JWT — looks like a raw GitHub token. Need to complete the auth flow first:

1. Open in browser → `http://localhost:9069/api/auth/github`
2. Complete GitHub OAuth → get redirected to frontend with `?code=XXX`
3. Exchange:
```bash
curl -s -X POST http://localhost:9069/api/auth/token -H "Content-Type: application/json" -d '{"code":"XXX"}'
```
4. Use `access_token` from the response as Bearer.

> DEVELOPER

omg ytou execute it and fix

> AGENT

Can't automate OAuth — it requires browser interaction. But let me check if there's a dev bypass or seed script.

> TOOL

tool_use Glob
id: toolu_014ZZVkNHWQyLqCV8nFPNetq
```json
{
  "pattern": "backend/scripts/**/*"
}
```

> TOOL

tool_use Glob
id: toolu_013GTx4Pt5qQcJgqmbcF3nAJ
```json
{
  "pattern": "scripts/**/*"
}
```

> TOOL

tool_result
id: toolu_013GTx4Pt5qQcJgqmbcF3nAJ
```
scripts/seed-github-test-org.sh
```

> TOOL

tool_result
id: toolu_014ZZVkNHWQyLqCV8nFPNetq
```
No files found
```

> TOOL

tool_use Grep
id: toolu_01MeA1443v5en4cgLTFDAJ1H
```json
{
  "pattern": "sign|jwt|generateToken|accessToken",
  "path": "backend/src/modules/auth/auth.service.ts",
  "output_mode": "content",
  "head_limit": 50
}
```

> TOOL

tool_result
id: toolu_01MeA1443v5en4cgLTFDAJ1H
```
4:import { JwtService } from '@nestjs/jwt';
49:		private readonly jwtService: JwtService,
117:		const { accessToken } = await strategy.validateAuthorizationCode({
122:		const profile = await strategy.getUserProfile({ accessToken });
160:				access_token: accessToken,
187:				access_token: accessToken,
217:	}): Promise<{ accessToken: string; refreshToken: string }> {
261:		const accessToken = await this.jwtService.signAsync(payload, {
265:		return { accessToken, refreshToken };
272:	}): Promise<{ accessToken: string; refreshToken: string }> {
325:		const accessToken = await this.jwtService.signAsync(payload, {
329:		return { accessToken, refreshToken: newRefreshToken };
```

> AGENT

No dev bypass exists. OAuth requires a browser — I can't automate that step. You need to:

1. Open `http://localhost:9069/api/auth/github` in your browser
2. Complete GitHub OAuth
3. Copy the `code` from the redirect URL (`/auth/callback?code=XXX`)
4. Run the token exchange curl → get the real JWT

That part is unavoidable.

> DEVELOPER

6e05e167a8f4d9b27721ba2f8b925562d14d89e5f968217aac6a82da79052a74

> TOOL

tool_use Bash
id: toolu_01GEj6ges7mJf8aBqeiV573X
```json
{
  "command": "curl -s -X POST http://localhost:9069/api/auth/token -H \"Content-Type: application/json\" -d '{\"code\":\"6e05e167a8f4d9b27721ba2f8b925562d14d89e5f968217aac6a82da79052a74\"}'",
  "description": "Exchange auth code for JWT"
}
```

> TOOL

tool_result
id: toolu_01GEj6ges7mJf8aBqeiV573X
```
{"access_token=[REDACTED].eyJ1c2VyX2lkIjoiZDBmNjc0M2EtNmU2YS00OGVhLWIyYzktMjFjZjk1MjZiMWI3Iiwic2Vzc2lvbl9pZCI6IjliYzY3ODFhLTFkNDQtNDdlOC1hMTVjLTY3ZDY3NGI3ZjllOSIsInJvbGUiOiJhZG1pbiIsImNvbXBhbnlfaWQiOiI5YjBiMTg4NC0yYTRlLTQ2ZWItODBlNy03MTBmYzRjYmMzZDkiLCJpYXQiOjE3NzYzNzY2MzAsImV4cCI6MTc3NjM4MDIzMH0.gewuUY046Vo_8C5hcmcNKVVnZmSl8nEkz1s1YQRZil4"}
```

> AGENT

Got the JWT. Triggering Jira connect:

> TOOL

tool_use Bash
id: toolu_01WC3ogruBhCAMPPZoY4hULZ
```json
{
  "command": "curl -s -X POST http://localhost:9069/api/integrations/jira/connect -H \"Authorization: bearer [REDACTED]\"",
  "description": "Initiate Jira OAuth connect"
}
```

> TOOL

tool_result
id: toolu_01WC3ogruBhCAMPPZoY4hULZ
```
{"url":"https://auth.atlassian.com/authorize?audience=api.atlassian.com&client_id=cfJ0AKtUWQGERXMzwsClf5QjLnOEWOj6&scope=read%3Ajira-work%20read%3Ajira-user%20offline_access&redirect_uri=https%3A%2F%2Fno-name-proj-1488-dev.loca.lt%2Fapi%2Fjira%2Fcallback&state=45394c34-d448-40aa-a29a-b66658e7408e&response_type=code&prompt=consent"}
```

> AGENT

Open this URL in your browser to authorize Jira:

```
https://auth.atlassian.com/authorize?audience=api.atlassian.com&client_id=cfJ0AKtUWQGERXMzwsClf5QjLnOEWOj6&scope=read%3Ajira-work%20read%3Ajira-user%20offline_access&redirect_uri=https%3A%2F%2Fno-name-proj-1488-dev.loca.lt%2Fapi%2Fjira%2Fcallback&state=45394c34-d448-40aa-a29a-b66658e7408e&response_type=code&prompt=consent
```

After authorizing, watch the backend logs for the installation upsert.

> DEVELOPER

gimme lienk as 1 row

> AGENT

`https://auth.atlassian.com/authorize?audience=api.atlassian.com&client_id=cfJ0AKtUWQGERXMzwsClf5QjLnOEWOj6&scope=read%3Ajira-work%20read%3Ajira-user%20offline_access&redirect_uri=https%3A%2F%2Fno-name-proj-1488-dev.loca.lt%2Fapi%2Fjira%2Fcallback&state=45394c34-d448-40aa-a29a-b66658e7408e&response_type=code&prompt=consent`

> DEVELOPER

/var/folders/0q/tm_g36415fvfqd294rghvdnw0000gn/T/TemporaryItems/NSIRD_screencaptureui_NueQl4/Screenshot\ 2026-04-16\ at\ 23.57.45.png

> TOOL

tool_use Read
id: toolu_015kCj27bhqHYUums1CawWbY
```json
{
  "file_path": "/var/folders/0q/tm_g36415fvfqd294rghvdnw0000gn/T/TemporaryItems/NSIRD_screencaptureui_NueQl4/Screenshot 2026-04-16 at 23.57.45.png"
}
```

> TOOL

tool_result
id: toolu_015kCj27bhqHYUums1CawWbY
```
{
  "type": "image",
  "source": {
    "type": "base64",
    "data": "iVBORw0KGgoAAAANSUhEUgAABwEAAALACAYAAAB7BQ0yAAABRWlDQ1BJQ0MgUHJvZmlsZQAAKJF9kEtLQkEYhh/rhNANCXe1cBF0wSIscieYhAQRYkXp7ng0DdSGc043+gutW7fqFwQugmjZNoKKfkLbwEUlp2+00i408M378M7LzDcfdBmmUmUDqFRdO51cCG1msiH/EwYBggwTNi1HxVOpZYnwqd9X/Q6f1tspfdfv839Xb77gWKJvUpOWsl3wjQun9l2l+UA4aEtTwseaiy0+1Zxr8Xkzs5ZOCF8LB6ySmRd+EA7nOvxiB1fKu9ZHD7r7/kJ1fVV0UGqECFGSsmdZYVFm83d2rplNsIPiEJttipRwCREXR1GmILxEFYtpwsIRZqTm9Yx/zq7t7cn/o6Py1Evbyyi4MGHopu2NxWDgCC5zyrTNr4n66oazNRtpcV8Nek4873kD/BPQuPe815rnNc6g+xGu6u/lvFoZ+E+pHwAAAFZlWElmTU0AKgAAAAgAAYdpAAQAAAABAAAAGgAAAAAAA5KGAAcAAAASAAAARKACAAQAAAABAAAHAaADAAQAAAABAAACwAAAAABBU0NJSQAAAFNjcmVlbnNob3Q9ykEYAAAB12lUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNi4wLjAiPgogICA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogICAgICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgICAgICAgICB4bWxuczpleGlmPSJodHRwOi8vbnMuYWRvYmUuY29tL2V4aWYvMS4wLyI+CiAgICAgICAgIDxleGlmOlBpeGVsWURpbWVuc2lvbj43MDQ8L2V4aWY6UGl4ZWxZRGltZW5zaW9uPgogICAgICAgICA8ZXhpZjpQaXhlbFhEaW1lbnNpb24+MTc5MzwvZXhpZjpQaXhlbFhEaW1lbnNpb24+CiAgICAgICAgIDxleGlmOlVzZXJDb21tZW50PlNjcmVlbnNob3Q8L2V4aWY6VXNlckNvbW1lbnQ+CiAgICAgIDwvcmRmOkRlc2NyaXB0aW9uPgogICA8L3JkZjpSREY+CjwveDp4bXBtZXRhPgrggx7lAABAAElEQVR4AeydB4AdVdXH7yabSkkgEDokofeioPRAEOkgVUEEUQRBKfqJIEVUmiBVUcEGKB1UulID0hGQ3kPohCQEEtKTzXd/d3Med4dp7+17u9nN/8Bm5s3cuXPnN7eec8+dpr322mvO6NGjnUQEREAEREAEREAEREAEREAEREAEREAEREAEREAEREAEREAEREAERKB7EGju1atX93gSPUW7CbS0tLiZM2e6WbNmudmzZzt+z5kzp93xKgIREAEREAEREAEREAEREAEREAEREAEREAEREAEREAEREIHGEGhqanI9evRwPXv2dM3NzQ67D78lItBMppDM3wQw/E2fPj0YAOdvEnp6ERABERABERABERABERABERABERABERABERABERABEehaBHDmwbGHvxkzZoTEYwjs06dPMAh2radRautJoLmekSmurkWACmHq1Kky/nWt16bUioAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiEAuAZx/+MMY2K9fv+AlmHuBTnZLAjICdsvXWvxQeP5NmTKlOKBCiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIdEkCZgzs379/8Azskg+hRNdMQIvC1oyu616I958MgF33/SnlIiACIiACIiACIiACIiACIiACIiACIiACIiACIiACIlANAWwC2AYk8xcBeQLOX+87FPJp06ZlPjXfiMQ9mI+Hsm8fD21paQnrCc+aNSu4ELOUqEQEREAEREAEREAEREAEREAEREAEREAEREAEREAEREAERKBrEDDbAMuDSuYPAjICzh/vOTwlS4BaIU8+Nga/vn37ut69eydPhd8YA/mz9YP5uChxyRiYiksHRUAEREAEREAEREAEREAEREAEREAEREAEREAEREAERGCeI4BeH11/nz595rm0KUH1JyAjYP2ZzpMxYqzLWgKUws56wNUIxkL+iBPjokQEREAEREAEREAEREAEREAEREAEREAEREAEREAEREAERGDeJ4Be31YDnPdTqxS2h4C+Cdgeel3o2qy1fvH+q9YAGD821xKHRAREQAREQAREQAREQAREQAREQAREQAREQAREQAREQAREoGsQyLIZdI3UK5VlCcgTsCypLhxu5syZ4Tt+yUfAA7Aea/8Sx5w5c+QRmASs3yIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiLQDgK77LKLe+mll8JfO6L5zKVmN+ATYI2SWbNmOYyNdi/uw/3ss2N4IzZSBg8e7FZddVU3duxYt/TSS7ullloq3HvcuHFuzJgxYbVDbBsmfDaNtJK+Dz/80D333HN2qm7bJh8Td1yiX7M7ZcOl3JWvfOjufm9yiH/xvs1u22UWdFe//rGb3TInhGvvjeUJ2F6CXeD6tOU6yczt8QBMPjZxEadEBERABERABERABERABERABERABERABERABERABERABESgfgQwBDZC0mwH9brP5MmT3SeffOK23HJL95PjfuL+/e9/u9tvv92dcMIJ4dikSZMcYRopSyyxhOMbiHvttZfbdddd3cCBA4NdZL/99nMbb7yx++ijj8K3ET/44AP35S9/2e25554OA2FTU5MbNGhQQ5JmJsc+PZrcgN7NbqulFnC95lrq1lm0r9tmmYVcs7cUEm4hvzPATtaYmoYYAb/0pS85/uYVWW655Rx/nS0rrriiO/TQQ91ZZ50V/mJO7HO83tLS0pLqBZi1hOeaa64ZCgSFolrJijMZDwXo5JNPdl/4wheSpyq/11prLffjH/+48rseO9///vfdF7/4xXpElRlHmWfLvHgePkH5+da3vhVmRswryaynEXteeabOSsc222wTGrl63p+ycNhhh7l11lmnntFW4uL9kyeXWWaZyrH27MQMGp32OJ3ca7XVVnPLL798fLhL79f73VQLgxleRx55pFtsscWqvbQSvh5xVCLr4J2VV145lA277W677eZ23nln+9mlt2nPsuiii4aOeTUPxsfP6WfwnrOE7x7TJ6KMxlJL3ujoNMbpbcR+LWWLVSPWW289t+CCC2YmiYHYsGHDMs/X+0Rafqr3PdobX1Z92hnvgLTss88+jv503nss88y1pL895bYoTeQ9+hSLL754CNpZeQOutazSAs+11147fM8l61lXWGGF1HYx7v9kXduZx5NjEPIB72ro0KGdmaxuf28UZfSlaL86SugLF+X/MmGK0ptVrxZdV/Y8ysR11123bPC6hqPfcsABBxTGWc9ytMEGGwQdV3zTOP7dd9/d7bjjjuF0LX2oON54HwXupptuGh+qaT9+X0l+8bmaIi+4aF6vfwuSr9MiIAKdQAADIN5sjRC83rAh1FvwoqOvevU117oRh57nnh+8n/vJI8PcsQ8PdU8O3Ndt449de931bskllwwed/W+v8WHtx9jmc997nPuL3/5i7v//vvdv/71L3fTTTeFPjRt1+zZs93CCy8cbEjo6egH4cHIXyPENA1vTp7pbh49wW241AC3njf+IYv17enemzLDTZs9xw3q09Od8YWl3XfXaO2X2XXVpqnuvpYYs7bddttg0a02MY0MbwrWt956q5G3yYwb4x9GwNdee63yB6dGC4U4KXjsodxKCoa/NdZYIxymA/T8889X5e5KnFjVKTR5gsstHTYK1iOPPJIadKONNnJ0is4888yw1GhqoJyDm2++uVt99dXdxRdfXAm10047uYUWWsg9/PDDlWP13inzbPW+Z0fEt91227kNN9zQ/elPf+qI2+Xe48ADDwzGXFzFyWuPP/54m/ece7FOhgYPJeu1115bobH11lsHF3dm49RLUKQxKESh9fTTT9cr2ko81B/M1nnllVfcO++8Uzle607MoBFpZ0D+0EMPuZdffrmSxCFDhoTJDrbkwsSJE91JJ50UZkhVAnXBnXq/m2oRMMEEZSidu7J5eocddggzz+69995wu1riqDadjQrPs1M2/vznP4f2k74GnXk6t42StPzdiHvFz0In/bTTTgsDCtqC88873z3/wvOV23796193W2yxhTvmmGPCrD47sf/++4fjZtxjRiLxMOPP5P/+7//C4IowxE2+uOKKK8LpavJGZ6XRnqM9W5ZIoU//97//3TEzE0EpzCQu6ixmah5//PFt6qtTTjklzKb8wQ9+ULk1YY877rg2Ex3eGP2GO/2M0yuDKfpmzAK1GZbMQr3kkkvcY489VomnETtxfiqKn/ok2XYWXVOP88n6tDPfwYknnuTL26BQntLGEWWet5b0E297y21R2lBMU28+8cQTYYmgavJGUdycT7Yxadcccsgh7vOf/3w4Rdt13XXXVYIxLjv66KNDP5y+hAnKEsrXAgssEA6xhNE999xTqa84yIQHxqE2WZNZztR5KGSQuP8TDqT8k1bHpx1LubTdh5JjECaX8a7uu+++dsetCLIJMHGW/gR9+TvvvDM7oD9DHc7kAOrIUaNGhfyVvGD99dd3hx9+eDh8+umnB30IP2hnv/vd7zrOW7tMm3Pe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gEqBmQH8SURABERABERABERABERABERABERABERABERABERABERABERABLouAZmCu+67U8pFQAREQAREQAREQAREQAREQAREQAREQAREQAREQAREQAREQAREIJWAjICpWHRQBERABERABERABERABERABERABERABERABERABERABERABERABLouARkBu+67U8pFQAREQAREQAREQAREQAREQAREQAREQAREQAREQAREQAREQAREIJWAjICpWHRQBERABERABERABERABERABERABERABERABERABERABERABERABLouARkBu+67U8pFQAREQAREQAREQAREQAREQAREQAREQAREQAREQAREQAREQAREIJWAjICpWHRQBERABERABERABERABERABERABERABERABERABERABERABERABLouARkBu+67U8pFQAREQAREQAREQAREQAREQAREQAREQAREQAREQAREQAREQAREIJWAjICpWHRQBERABERABERABERABERABERABERABERABERABERABERABERABLouARkBu+67U8pFQAREQAREQAREQAREQAREQAREQAREQAREQAREQAREQAREQAREIJVAc+rRxMEttxrhttlmW7fccsslzlT/86233nJ33nm7u/eeu6q/2F+x/fJLuR2HLetWGLiwa6ophsZdNMdH/cZHE90to952t735Xk036jOnxfHX7Iit8TLLU5ze1CP81XK3Zdfd2Q3ZYDc3YPFhru4vxCP4eOwoN/qJf7q3n7qpluTpGhEQAREQAREQAREQAREQAREQAREQAREQAREQAREQAREQARGYLwk07b///nNefPHF1IdfYskl3QEHfMtNmTrFPXD/f9xrr72aGq6agyuuuJLbdLPNXf9+/d2ll/7JjXn//VKXL71AX3f4Oqu6KTNmurtGveleHj+h1HUdHWiVQYu4EcOWd/1793IXPv2Se3fytFJJ6OGNfgu0tLherqVU+HoHmul6uMk9evi7lzOt9l9kWbfWtke76dOmuNFP3+4+fOcln6R6Gy6b3KLLrOqGrLOt69O3v3v29nPdlAlv1/vRFZ8IiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIdDsCuUbAY358vHv55Zfc3XffWfcH33rrbdwqq6zqzvzlqaXiPnXjdd3zH4xz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989//tOiDdsDDjjA8W5PO+00N2HCp98tL1u/FvU3kvURbda///1v95///KdNOqot220u1g8REAEREAEREAEREAEREAEREIFuSSDTCFj0tL/wirQhQ4e4J5980t3hPZE23HBDt9XWW7vT/AD9KK/sbpqrHEhTJRTFnTxfJo6VvBcfBkBk9+23c2f+/qI20aDASpOfHnWkW80bgZ7xir/b/UB6da8g2H6r4e7M449zX/veEeGSnx19VAjz3Msvu3/5WeSrrbiS22Hr1jAYFid9ku1BUibtaemKj4166y33b3/f5Zdexm27xebuqG8f5P779NNu2owZIdgbXpFxTzSj/KW5SpY9d9jBjdh0UzfGe8ZcdeNNbtFFBrqvecXdGcf+2O1z+Pdq90QKD4VCKFt69erlNvziZu6xhz9dnmyn3fYOF8ya6zFqCp7yjPw9ywfOTlwXPpM0UNqjoHDnL0uq8RZcwZclZryjYDLZaaedwu6MuXmOH/b+LEwjth3xvMnniH+fffbZDs81vAQw4mG0w3gSe1HF4bMY7LnnnkGBeO655wYPOBTSKLwff/zxYHTIuq6W4x3BzOpT8gjGt3XWWcc97eskk/XWWy9wQ/GLwPAHP/hB8LjD0Pb666+HNuMrX/mK23///d1f/vIXu7TNFgPBSy+9FI4RDmPq73//+/Abz71ll13WoXjFG4l384n3dN5uu+3cZptt5iZOnOjuueeeNvHFP4gPOfnkk4MhDOMthj8MmyYonKnLVl999aCYPuqoo4LyOlbwWtj2bBv9zr773e8GA+BVV13lMD6j+N5vv/3ct771raBcJ+1l8nG1z9jI5/rb3/7m+vXrF5L0wx/+MHiomUHqo48+CsfLPNMkP+kHoyF1HkZn8g5GCPIO12MUNCMVkcb1ItfGEybieiEkoEH/zOqxkHtv0DfcrJ6tk4ya/fcAF5tU3hsco4YZv5kEw3sqEjyXMXC214OZOgFjDfffcsst3SabbBIM7xhmGynXXnutu/766+t+i856nno8yD6zWw2As/xS8D1854rv/7X27JiUwcQx+s2tR+h68dfify/sj3/NX5tnBPRBQ7lhssjyyy/v9tprL/f1r3/d/fznP+dUEMoV5cuEOp1yiAHwqaeecldeeWUwwlPvfuMb3wjGNTMCftFPbhs+fLg744wzwuVxueQAZZN6mjJNO2Ky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BERABERABERABERABERABERABERg3idQygg47z+GUigCIiACIiACIiACIiACIiACIiACIiACIiACIiACIiACIiACIiACImAEetiOtiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAt2DgIyA3eM96ilEQAREQAREQAREQAREQAREQAREQAREQAREQAREQAREQAREQAREoEJARsAKCu2IgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIQPcgICNg93iPegoREAEREAEREAEREAEREAEREAEREAEREAEREAEREAEREAEREAERqBCQEbCCQjsiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIi0D0IyAjYPd6jnkIEREAEREAEREAEREAEREAEREAEREAEREAEREAEREAEREAEREAEKgRkBKyg0I4IiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIdA8CMgJ2j/eopxABERABERABERABERABERABERABERABERABERABERABERABERCBCgEZASsotCMCIiACIiACIiACIiACIiACIiACIiACIiACIiACIiACIiACIiAC3YNAc+++fVyffn27x9PoKURABERABERABERABERABERABERABERABERABERABERABERABERABFzTHC/iIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIi0H0IaDnQ7vMu9SQiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiEAjICKiMIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIAIiIALdjICMgN3shepxREAEREAEREAEREAEREAEREAEREAEREAEREAEREAEREAEREAEREBGQOUBERABERABERABERABERABERABERABERABERABERABERABERABEehmBGQE7GYvVI8jAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAjICKg+IgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIQDcjICNgN3uhehwREAEREAEREAEREAEREAEREAEREAEREAEREAEREAEREAEREAERkBFQeUAEREAEREAEREAEREAEREAEREAEREAEREAEREAEREAEREAEREAEuhkBGQG72QvV44iACIiACIiACIiACIiACIiACIiACIiACIiACIiACIiACIiACIiAjIDKAyIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiIgAiLQzQjICNjNXqgeRwREQAREQAREQAREQAREQAREQAREQAREQAREQAREQAREQAREQARkBFQeEAEREAEREAEREAEREAEREAEREAEREAEREAEREAEREAEREAER+H/27i5GvvM8DPvsX3TtVJTbAo6YOL2xSNmsA4l24PAfQEAuYte56IV8URcB7Nh1jQIJIMko4MjoRQPDN6mVDyCUEilVZdWSXQRN2oYXQRBHCQoXAkrKtUUqdihZopw6KUlFrt2QAqoP7vR9nvd9z5ydPWd3dmf3v/PxO8uZ8573+/zO8IJ4+MwQODABQcADe6BuhwABAgQIECBAgAABAgQIECBAgAABAgQIECBAgIAgoM8AAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAgQMTEAQ8sAfqdggQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgIAvoMECBAgAABAgQIECBAgAABAgQIECBAgAABAgQIEDgwAUHAA3ugbocAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQICAIKDPAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAIEDExAEPLAH6nYIECBAgAABAgQIECBAgAABAgQIECBAgAABAgQICAL6DBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBA4MAFBwAN7oG6HAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAgCCgzwABAgQIECBAgAABAgQIECBAgAABAgQIECBAgACBAxMQBDywB+p2CBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECAgC+gwQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQODABQcADe6BuhwABAgQIECBAgAABAgQIECBAgAABAgQIECBAgIAgoM8AAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAgQMTEAQ8sAfqdggQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgIAvoMECBAgAABAgQIECBAgAABAgQIECBAgAABAgQIEDgwAUHAA3ugbocAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQICAIKDPAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAIEDExAEPLAH6nYIECBAgAABAgQIECBAgAABAgQIECBAgAABAgQICAL6DBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBA4MAFBwAN7oG6HAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAgCCgzwABAgQIECBAgAABAgQIECBAgAABAgQIECBAgACBAxMQBDywB+p2CBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECAgC+gwQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQODABQcADe6BuhwABAgQIECBAgAABAgQIECBAgAABAgQIECBAgIAgoM8AAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAgQMTEAQ8sAfqdggQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgIAvoMECBAgAABAgQIECBAgAABAgQIECBAgAABAgQIEDgwAUHAA3ugbocAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQICAIKDPAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAIEDExAEPLAH6nYIECBAgAABAgQIECBAgAABAgQIECBAgAABAgQICAL6DBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBA4MAFBwAN7oG6HAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAgCCgzwABAgQIECBAgAABAgQIECBAgAABAgQIECBAgACBAxMQBDywB+p2CBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECAgC+gwQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQODABQcADe6BuhwABAgQIECBAgAABAgQIECBAgAABAgQIECBAgIAgoM8AAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAgQMTEAQ8sAfqdggQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgIAvoMECBAgAABAgQIECBAgAABAgQIECBAgAABAgQIEDgwAUHAA3ugbocAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQICAIKDPAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAIEDExAEPLAH6nYIECBAgAABAgQIECBAgAABAgQIECBAgAABAgQICAL6DBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBA4MAFBwAN7oG6HAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAgCCgzwABAgQIECBAgAABAgQIECBAgAABAgQIECBAgACBAxMQBDywB+p2CBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECAgC+gwQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQODABQcADe6BuhwABAgQIECBAgAABAgQIECBAgAABAgQIECBAgIAgoM8AAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAgQMTEAQ8sAfqdggQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgIAvoMECBAgAABAgQIECBAgAABAgQIECBAgAABAgQIEDgwAUHAA3ugbocAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQICAIKDPAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAIEDExAEPLAH6nYIECBAgAABAgQIECBAgAABAgQIECBAgAABAgQICAL6DBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBA4MAFBwAN7oG6HAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAgCCgzwABAgQIECBAgAABAgQIECBAgAABAgQIECBAgACBAxMQBDywB+p2CBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECAgC+gwQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQODABQcADe6BuhwABAgQIECBAgAABAgQIECBAgAABAgQIECBAgIAgoM8AAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAgQMTEAQ8sAfqdggQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgIAvoMECBAgAABAgQIECBAgAABAgQIECBAgAABAgQIEDgwAUHAA3ugbocAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQICAIKDPAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAIEDExAEPLAH6nYIECBAgAABAgQIECBAgAABAgQIECBAgAABAgQICAL6DBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBA4MAFBwAN7oG6HAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAgCCgzwABAgQIECBAgAABAgQIECBAgAABAgQIECBAgACBAxMQBDywB+p2CBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECAgC+gwQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQODABQcADe6BuhwABAgQIECBAgAABAgQIECBAgAABAgQIECBAgIAgoM8AAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAgQMTEAQ8sAfqdggQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgIAvoMECBAgAABAgQIECBAgAABAgQIECBAgAABAgQIEDgwAUHAA3ugbocAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQICAIKDPAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAIEDExAEPLAH6nYIECBAgAABAgQIECBAgAABAgQIECBAgAABAgQICAL6DBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBA4MAFBwAN7oG6HAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAgCCgzwABAgQIECBAgAABAgQIECBAgAABAgQIECBAgACBAxMQBDywB+p2CBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECAgC+gwQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQODABQcADe6BuhwABAgQIECBAgAABAgQIECBAgAABAgQIECBAgIAgoM8AAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAgQMTEAQ8sAfqdggQIECAAAECBAgQIECAAAECBAgQIECAAAECBAgIAvoMECBAgAABAgQIECBAgAABAgQIECBAgAABAgQIEDgwAUHAA3ugbocAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQICAIKDPAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAIEDExAEPLAH6nYIECBAgAABAgQIELh9gfc9/aXbX8QKBAgQIECAAAECBAgQIEBgCwFBwC3wDCVAgAABAgQIECBA4PgEIgD4vn/wyuKdP//i8d28OyZAgAABAgQIECBAgACBvREQBNybR2WjBAgQIECA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IECAAAECBAgQIECAAAECBAgQIECAAAECBAgQ2EEBQcAdfCi2RIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQGAbAUHAbfSMJUCAAAECBAgQIECAAAECBAgQIECAAAECBAgQILCDAoKAO/hQbIkAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIDANgKCgNvoGUuAAAECBAgQIECAAAECBAgQIECAAAECBAgQIEBgBwUEAXfwodgSAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAgW0EBAG30TOWAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAwA4KCALu4EOxJQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQLbCAgCbqNnLAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAIEdFBAE3MGHYksECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIEthEQBNxGz1gCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECOyggCLiDD8WWCBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECGwjIAi4jZ6xBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBHZQQBBwBx+KLREgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBDYRkAQcBs9YwkQIECAAAECBAgQIECAAAECBAgQIECAAAECBAjsoIAg4A4+FFsiQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgsI2AIOA2esYSIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQ2EEBQcAdfCi2RIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQGAbAUHAbfSMJUCAAAECBAgQIECAAAECBAgQIECAAAECBAgQILCDAoKAO/hQbIkAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIDANgKCgNvoGUuAAAECBAgQIECAAAECBAgQIECAAAECBAgQIEBgBwUEAXfwodgSAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAgW0EBAG30TOWAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAwA4KCALu4EOxJQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQLbCAgCbqNnLAECBAgQIECAAAECBAgQIECAAAECBAgQ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xvLWr4fz0HDJvupmhvXLAn3deo55xnvu5Tqu7qfXTewjh7e+o/IqaFna3vTE4iQyAAUAQ8hBgAABAgQIECBAgMCMgCDgDIxqAgQIECBAgAABAgQIEFgJRDDw9EvPLJblVY8IZGXYa7jMwrmgWu/eAls9vtX7RXNMVf56EK2e43pZYnXDgLPXvX5o7oVN1hv1bfPEabVu20+pqz2HQqmoNbVhqjyui3vr1+2c2yvlfjms3++/nUu/cvc5/ORN3zPMc/Lt/3kGAXMabwQIECBAgAABAgQIELhAQBDwAhxNBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBPZR4N4+btqeCRAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBCYFxAEnLfRQoAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQGAvBQQB9/Kx2TQBAgQIECBAgAABAgQIECBAgAABAgQIECBAgACBeQFBwHkbLQQIECBAgAABAgQIECBAgAABAgQIECBAgAABAgT2UkAQcC8fm00TIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQmBcQBJy30UKAAAECBAgQIECAAAECBAgQIECAAAECBAgQIEBgLwUEAffysdk0AQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAgXkBQcB5Gy0ECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIE9lJAEHAvH5tNEyBAgAABAgQIECBAgAABAgQIECBAgAABAgQIEJgXEASct9FCgAABAgQIECBAgAABAgQIECBAgAABAgQIECBAYC8FBAH38rHZNAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAIF5AUHAeRstBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBPZSQBBwLx+bTRMgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBCYFxAEnLfRQoAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQGAvBQQB9/Kx2TQBAgQIECBAgAABAgQIECBAgAABAgQIECBAgACBeQFBwHkbLQQIECBAgAABAgQIECBAgAABAgQIECBAgAABAgT2UkAQcC8fm00TIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQmBcQBJy30UKAAAECBAgQIECAAAECBAgQIECAAAECBAgQIEBgLwUEAffysdk0AQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAgXkBQcB5Gy0ECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIE9lJAEHAvH5tNEyBAgAABAgQIECBAgAABAgQIECBAgAABAgQIEJgXEASct9FCgAABAgQIECBAgAABAgQIECBAgAABAgQIECBAYC8FBAH38rHZNAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAIF5AUHAeRstBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBPZSQBBwLx+bTRMgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBCYFxAEnLfRQoAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQGAvBQQB9/Kx2TQBAgQIECBAgAABAgQIECBAgAABAgQIECBAgACBeQFBwHkbLQQIECBAgAABAgQIECBAgAABAgQIECBAgAABAgT2UkAQcC8fm00TIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQmBcQBJy30UKAAAECBAgQIECAAAECBAgQIECAAAECBAgQIEBgLwUEAffysdk0AQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAgXkBQcB5Gy0ECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIE9lJAEHAvH5tNEyBAgAABAgQIECBAgAABAgQIECBAgAABAgQIEJgXEASct9FCgAABAgQIECBAgAABAgQIECBAgAABAgQIECBAYC8FBAH38rHZNAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAIF5AUHAeRstBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBPZSQBBwLx+bTRMgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBCYFxAEnLfRQoAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQGAvBQQB9/Kx2TQBAgQIECBAgAABAgQIECBAgAABAgQIECBAgACBeQFBwHkbLQQIECBAgAABAgQIECBAgAABAgQIECBAgAABAgT2UkAQcC8fm00TIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQmBcQBJy30UKAAAECBAgQIECAAAECBAgQIECAAAECBAgQIEBgLwUEAffysdk0AQIECBAgQIAAAQIECBAgQIAA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SIAEIpIARcCIpMu6SYAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESOApEKAI+BSgs0kSIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESiEgCFAEjki7rJgESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIIGnQIAi4FOAziZJgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIICIJUASMSLqsmwRIgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgASeAgGKgE8BOpskARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIggYgkQBEwIumybhIgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgARJ4CgQoAj4F6GySBEiABEiABEiABEiABEiABEiABEiABEiABEiABEiABEiABEiABCKSAEXAiKTLukmABEiABEiABEiABEiABEiABEiABEiABEiABEiABEiABEiABEjgKRCgCPgUoLNJEiABEiABEiABEiABEiABEiABEiABEiABEiABEiABEiABEiABEohIAhQBI5Iu6yYBEiABEiABEiABEiABEiABEiABEiABEiABEiABEiABEiABEiCBp0CAIuBTgM4mSYAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESCAiCVAEjEi6rJsESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAEngIBioBPATqbJAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIIGIJEARMCLpsm4SIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESeAoEKAI+BehskgRIgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgAQikgBFwIiky7pJgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgARI4CkQoAj4FKCzSRIgARIgARIgARIgARIgARIgARIgARIgARIg/JsF8QAAQABJREFUARIgARIgARIgARKISAIUASOSLusmARIgARIgARIggadA4NSpUzJv3vyn0HJgNXnz5k2ZOXOWXLt2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55ivejzl+xor3Gt4djrnOerDubhX3N3H9vaehee/vT/+7PvzHHJXj7fxspf39Izx5z571GdMWL4DfZXFvQgza4Xar80dO3dp9nM87V+6dEkL3QhDa0LMmlDr27ZtEnjeGsPzHf/uMt9FJh1tO9NMHrckQAIkQAIkQALPNgF6Aj7b48PekQAJkAAJkAAJkECEEvD3pSpeINtfErnrFF4OQST0Zv4KeqgDoo074cZT/Z6uxZ++e6oT6XiBb3+Jby8LMdOXoOmpX/Z6/N2HoJAmTWp/i0dIubCOS3h0wt26c/7WGzNmTI9F/X2hifE3YdE8VQYB73HG2qyXaer3Z966e3Fszse1+bo+Z5vmXG9bXKevZ4E535/7A8KHL/HD3/bQrrf71fTrccYpLOd6Gx/0xdczMyyszbU5t+7Y+uqXs47wPHbXH1/1Y0xfeukFX8W85nsbt+B7N7R3odcKHZm+xgr3mjsBENXgXH+4PAvPf8dl+zz05znkrhJv42Uv788zxtd9hvrC8owJy3egr7Le7kV37Nyl2Xl42kdUAIQdnT5jho44cOm33/Xazoho4Lx2T/+OQ9s0EiABEiABEiCBwCQQpauywOw6e00CJEACJEACJEACJPC0CeClUNJkSQWhMj0JZRBwMr6RUZInS/a0u8v2SYAEngECeHGfNl1ayZgxg8feYA3Q7NnfDvWC2uMJAZLhzzMzQC6F3SSBZ5aAP/fZf/UZ425QIDQj9Ozrr6eSKFGjSKY33pDGnzWUqp9UcVecaSRAAiRAAiRAAv8xAgwH+h8bUF4OCZAACZAACZAACZAACZAACZAACZAACZAACZAACZAACZAACZAACXhfxIF8SIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAEAo4ARcCAGzJ2mARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgAS8E6AI6J0Pc0mABEiABEiABEiABEiABEiABEiABEiABEiABEiABEiABEiABEgg4AhQBAy4IWOHSYAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESMA7AYqA3vkwlwRIgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgAQCjgBFwIAbMnaYBEiABEiABEiABEiABEiABEiABEiABEiABEiABEiABEiABEiABLwToAjonQ9zSYAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESCDgCFAEDLghY4dJgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIwDsBioDe+TCXBEiABEiABEiABEiABEiABEiABEiABEiABEiABEiABEiABEiABAKOAEXAgBsydpgESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAEvBOgCOidD3NJgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIIOAIUAQMuCFjh0mABEiABEiABEiABEiABEiABEiABEiABEiABEiABEiABEiABEjAOwGKgN75MJcESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAEAo4ARcCAGzJ2mARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgAS8E6AI6J0Pc0mABEiABEiABEiABEiABEiABEiABEiABEiABEiABEiABEiABEgg4AhQBAy4IWOHSYAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESMA7AYqA3vkwlwRIgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgAQCjgBFwIAbMnaYBEiABEiABEiABEiABEiABEiABEiABEiABEiABEiABEiABEiABLwToAjonQ9zSYAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESCDgCFAEDLghY4dJgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIwDsBioDe+TCXBEiABEiABEiABEiABEiABEiABEiABEiABEiABEiABEiABEiABAKOAEXAgBsydpgESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAEvBOgCOidD3NJgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIIOAIUAQMuCFjh0mABEiABEiABEiABEiABEiABEiABEiABEiABEiABEiABEiABEjAOwGKgN75MJcESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAESIAEAo4ARcCAGzJ2mARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgARIgAS8E6AI6J0Pc0mABEiABEiABEiABEiABEiABEiABEiABEiABEiABEiABEiABEgg4AhQBAy4IWOHSYAESIAESIAESIAESIAEHoXAmjVr5cqVK15PvXHjhty/fz9UGaT99ttv8uDBg1B5/ib88cdl+emndf4W91nu77//lps3b/osF6gF9u7dJydOnPTa/X///Vd+//13+euvv6xyYLJixUr5559/rLTw3AH327fvuK0S88PXHHN74iMm+pqX4PPnn396rP3y5cvhygntXb16VfG5HW5t+jMPPDb2MOPOnTuyefMWCQpa8Vj3sK92mE8CJEACJEACJEACJEACzxoBioDP2oiwPyRAAiRAAiRAAiRAAiRAAhFCoEXLVnL8+Am3dZ89e07q1msgOXLklpy58kj7Dp0scWT2nLmSKdNbUrBgEXknZ26d504oHDVqjKRPn0k2btzkto3jx49Ls+YtrDyIVwMGDpJs2d/RdVoZPnYgQrVt215y5c4r2bPnkoYNP5NLly75OCs421ObEG/Qd+ene4+e+kQIaqtXr5HKlavqMuAVHuapP6h74qTJsnx5kMdmli0Lkuw5ckqBAoXl7bffsQTWixcvyZdfNnkksQfi1dQfpkmhQkX0x9n48OEjJXPmrJI1a3Zp0rS5QFwyNm7ceClSpJjkyVNASpcuK2fOnDVZj7zt2bN3qDExlfmal+D37rtFJVeufFKxUmXZum2bOVXWrv1Jp+XNW1ByvJNL1q3fYOU96s6BAwd0e7lz51d8csjXTZrJhQsXrOoetU1f8wANYP7WrFVHs3IKkBCF8+YrIKPHjJVVag5HlDhsXSh3SIAESIAESIAESIAESOAZIkAR8BkaDHaFBEiABEiABEiABEiABEjg6RAYNnyE9ibbvXu7LFwwX+bMnisbHop5Wd96S4lRi+Xw4f0yY8Y0WbZsWShx6tSpUzJ9+owwdb527Xry888/S+rUqeWBG+9DT5UtXLhI5s37URYvXii7dm3Tnl5Tpk7zVNwl3VObkSJFkg0b1sr69Wv0Z9myxfq8QgUL6u1q5UXZslVreSPTG/oYokt4mKf++Kr79Okz0kSJTJ06dpD9+3fLunVrJF36dL5O85k/+Nuh8v33U+TtbG/LPSW22m3Xrt0ydOhw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wlKvPvdvb765+51u3doJiJYT1vwYS3euPm+cdubM2enRRx+ZXnrpV/NysZ+axj3zxIWvjUNL8Hrx4sWlHj+uPbe9BLejHt/n21e+Ocplr8IXX7w1XX32O9Pp0ztPIY79Hn89X/Og1y/me3J7+/u7p924sT19/O7Spevuy5MnT07feObyvFTs9SXEG/v4/fj5Hy6B97jYK/O9NwLm8RrHxvdbuV258q3phRd+Ov3s5s+XY2Pfv9Wxc+e+tCzxurm5M//x/hHgfX7u94+vvroEyC+//Jtp/Fu9Xn/9tZ0nRNd85vXta0ufX/zCudXblj0pT21sLMHk/7oPdk8excG32z2n+4UAAQIECBAgQIDAgyDwkXlZj511PR6EbvVIgAABAgQIECBAgMADL/DOO+8uocbRox+9z2IcG0srHj58+J5jY5/A8dTTJ+dlKA8dOnTPsYN+GXuejf/tOnbs6EGn3nd8PG3197femh46fnx3+c/VSePJxP/Me7X9P9ddXePD/O/wOXLkyLJP4Yd53dHnu/OTafs9yTeeknzvvWFwbN+PHHvuHZ/t3j/PfU/+gH/899gjb/5O7w9K181qdemxhOk4bywT+kGe3Bz3ze3bt5en8sa9N54s3Ps66L4cy3m+/fY/5s/72N63LfWwGdc7ceLEfcdWT/ntZz5OvnPnzjTePwxWy9Led5F9/rDuM8fp/5qfiP3n/DTuJ+YAfexduPe17j7Ye56aAAECBAgQIECAAIEICAFjoSJAgAABAgQIECBAgAABAgQIECBAgAABAgQIECBQIWBPwIoxaoIAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIBABISAsVARIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQqBAQAlaMURMECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIEIiAEjIWKAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAQIWAELBijJogQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgEAEhYCxUBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBCoEhIAVY9QEAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAgQgIAWOhIkCAAAECBAgQIECAAAECBAgQIECAAAECBAgQIFAhIASsGKMmCBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECERACBgLFQECBAgQIECAAAECBAgQIECAAAECBAgQIECAAIEKASFgxRg1QYAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQCACQsBYqAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAhUCAgBK8aoCQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIREALGQkWAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECgQkAIWDFGTRAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBCIgBAwFioCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECFQJCwIoxaoIAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIBABISAsVARIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQqBAQAlaMURMECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIEIiAEjIWKAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAQIWAELBijJogQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgEAEhYCxUBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBCoEhIAVY9QEAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAgQgIAWOhIkCAAAECBAgQIECAAAECBAgQIECAAAECBAgQIFAhIASsGKMmCBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECERACBgLFQECBAgQIECAAAECBAgQIECAAAECBAgQIECAAIEKASFgxRg1QYAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQCACQsBYqAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAhUCAgBK8aoCQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIREALGQkWAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECgQkAIWDFGTRAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBCIgBAwFioCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECFQJCwIoxaoIAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIBABISAsVARIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQqBAQAlaMURMECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIEIiAEjIWKAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAQIWAELBijJogQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgEAEhYCxUBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBCoEhIAVY9QEAQIECNtyX/4AAA2JSURBVBAgQIAAAQIECBAgQIAAAQIECBAgQIAAgQgIAWOhIkCAAAECBAgQIECAAAECBAgQIECAAAECBAgQIFAhIASsGKMmCBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECERACBgLFQECBAgQIECAAAECBAgQIECAAAECBAgQIECAAIEKASFgxRg1QYAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQCACQsBYqAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAhUCAgBK8aoCQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIREALGQkWAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECgQkAIWDFGTRAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBCIgBAwFioCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECFQJCwIoxaoIAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIBABISAsVARIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQqBAQAlaMURMECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIEIiAEjIWKAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAQIWAELBijJogQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgEAEhYCxUBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBCoEhIAVY9QEAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAgQgIAWOhIkCAAAECBAgQIECAAAECBAgQIECAAAECBAgQIFAhIASsGKMmCBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECERACBgLFQECBAgQIECAAAECBAgQIECAAAECBAgQIECAAIEKASFgxRg1QYAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQCACQsBYqAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAhUCAgBK8aoCQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIREALGQkWAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECgQkAIWDFGTRAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBCIgBAwFioCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECFQJCwIoxaoIAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIBABISAsVARIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQqBAQAlaMURMECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIEIiAEjIWKAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAQIWAELBijJogQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgEAEhYCxUBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBCoEhIAVY9QEAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAgQgIAWOhIkCAAAECBAgQIECAAAECBAgQIECAAAECBAgQIFAhIASsGKMmCBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECERACBgLFQECBAgQIECAAAECBAgQIECAAAECBAgQIECAAIEKASFgxRg1QYAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQCACQsBYqAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAhUCAgBK8aoCQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIREALGQkWAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECgQkAIWDFGTRAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBCIgBAwFioCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECFQJCwIoxaoIAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIBABISAsVARIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQqBAQAlaMURMECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIEIiAEjIWKAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAQIWAELBijJogQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgEAEhYCxUBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBCoEhIAVY9QEAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAgQgIAWOhIkCAAAECBAgQIECAAAECBAgQIECAAAECBAgQIFAhIASsGKMmCBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECERACBgLFQECBAgQIECAAAECBAgQIECAAAECBAgQIECAAIEKASFgxRg1QYAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQCACQsBYqAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAhUCAgBK8aoCQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIREALGQkWAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECgQkAIWDFGTRAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBCIgBAwFioCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECFQJCwIoxaoIAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIBABISAsVARIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQqBAQAlaMURMECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIEIiAEjIWKAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAQIWAELBijJogQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgEAEhYCxUBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBCoEhIAVY9QEAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAgQgIAWOhIkCAAAECBAgQIECAAAECBAgQIECAAAECBAgQIFAhIASsGKMmCBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECERACBgLFQECBAgQIECAAAECBAgQIECAAAECBAgQIECAAIEKASFgxRg1QYAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQCACQsBYqAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAhUCAgBK8aoCQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIREALGQkWAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECgQkAIWDFGTRAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBCIgBAwFioCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECFQJCwIoxaoIAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIBABISAsVARIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQqBAQAlaMURMECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIEIiAEjIWKAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAQIWAELBijJogQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgEAEhYCxUBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBCoEhIAVY9QEAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAgQgIAWOhIkCAAAECBAgQIECAAAECBAgQIECAAAECBAgQIFAhIASsGKMmCBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECERACBgLFQECBAgQIECAAAECBAgQIECAAAECBAgQIECAAIEKASFgxRg1QYAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQCACQsBYqAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBAhUCAgBK8aoCQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIREALGQkWAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECgQkAIWDFGTRAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBCIgBAwFioCBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECFQJCwIoxaoIAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIBABISAsVARIECAAAECBAgQIECAAAECBAgQIECAAAECBAgQqBAQAlaMURMECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIEIiAEjIWKAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAQIWAELBijJogQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgEAEhYCxUBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBCoEhIAVY9QEAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAgQgIAWOhIkCAAAECBAgQIECAAAECBAgQIECAAAECBAgQIFAhIASsGKMmCBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECERACBgLFQECBAgQIECAAAECBAgQIECAAAECBAgQIECAAIEKgf8CwaKAfCRlFqMAAAAASUVORK5CYII=",
    "media_type": "image/png"
  }
}
```

> AGENT

The redirect URI `https://no-name-proj-1488-dev.loca.lt/api/jira/callback` isn't registered in the Atlassian app. You need to add it in the Atlassian developer console:

1. Go to [developer.atlassian.com](https://developer.atlassian.com) → your app
2. **Authorization** → **Add callback URL**: `https://no-name-proj-1488-dev.loca.lt/api/jira/callback`
3. Save, then retry

> DEVELOPER

where to add callback there?

> TOOL

tool_use Read
id: toolu_016oSjQScHFJdSuFuhyDGAaf
```json
{
  "file_path": "/home/<USER>/Documents/repo/no-name-proj/backend/src/modules/jira/jira-install.service.ts"
}
```

> TOOL

tool_result
id: toolu_016oSjQScHFJdSuFuhyDGAaf
```
1	import { randomUUID } from 'node:crypto';
2	
3	import { InjectQueue } from '@nestjs/bullmq';
4	import { BadRequestException, Injectable, Logger } from '@nestjs/common';
5	import { Queue } from 'bullmq';
6	
7	import { CacheService } from '@modules/cache/cache.service';
8	import { Namespaces } from '@modules/cache/types/cache.interface';
9	import { EnvConfigService } from '@modules/env-config/env-config.service';
10	import { JiraInstallationModel } from '@modules/jira/db/jira-installations.model';
11	import { JiraApiService } from '@modules/jira/jira-api.service';
12	import { IJiraInstallationBase } from '@modules/jira/types/jira-installation.interface';
13	
14	import { JIRA_CLIENT_ID, JIRA_CALLBACK_URL } from '@constants/env-variables.constant';
15	
16	interface IInstallStateValue {
17		companyId: string;
18		userId: string;
19	}
20	
21	const STATE_TTL_MS = 5 * 60 * 1000;
22	const ATLASSIAN_AUTH_URL = 'https://auth.atlassian.com/authorize';
23	
24	@Injectable()
25	export class JiraInstallService {
26		private readonly logger = new Logger(JiraInstallService.name);
27	
28		constructor(
29			private readonly configService: EnvConfigService,
30			private readonly cacheService: CacheService,
31			private readonly jiraApiService: JiraApiService,
32			private readonly installationModel: JiraInstallationModel,
33			@InjectQueue('jira') private readonly jiraQueue: Queue,
34		) {}
35	
36		async initiateConnect({
37			companyId,
38			userId,
39		}: {
40			companyId: string;
41			userId: string;
42		}): Promise<string> {
43			const state = randomUUID();
44	
45			await this.cacheService.set({
46				namespace: Namespaces.JIRA_INSTALL_STATE,
47				key: state,
48				value: […]

> AGENT

The callback URL comes from `JIRA_CALLBACK_URL` env var. To register it in Atlassian:

1. Go to `https://developer.atlassian.com/console/myapps/`
2. Click your app
3. **Authorization** (left sidebar) → **Add** next to "OAuth 2.0 (3LO)"
4. Set callback URL to: `https://no-name-proj-1488-dev.loca.lt/api/jira/callback`
5. Save

> DEVELOPER

saved

> AGENT

Get a fresh OAuth URL (state expired):

> TOOL

tool_use Bash
id: toolu_01VvjnhwrTjXj1sEU5wZatbZ
```json
{
  "command": "curl -s -X POST http://localhost:9069/api/integrations/jira/connect -H \"Authorization: bearer [REDACTED]\"",
  "description": "Get fresh Jira OAuth URL"
}
```

> TOOL

tool_result
id: toolu_01VvjnhwrTjXj1sEU5wZatbZ
```
{"url":"https://auth.atlassian.com/authorize?audience=api.atlassian.com&client_id=cfJ0AKtUWQGERXMzwsClf5QjLnOEWOj6&scope=read%3Ajira-work%20read%3Ajira-user%20offline_access&redirect_uri=https%3A%2F%2Fno-name-proj-1488-dev.loca.lt%2Fapi%2Fjira%2Fcallback&state=7c3ad3ff-17b2-4c72-9c8b-401c9b201719&response_type=code&prompt=consent"}
```

> AGENT

`https://auth.atlassian.com/authorize?audience=api.atlassian.com&client_id=cfJ0AKtUWQGERXMzwsClf5QjLnOEWOj6&scope=read%3Ajira-work%20read%3Ajira-user%20offline_access&redirect_uri=https%3A%2F%2Fno-name-proj-1488-dev.loca.lt%2Fapi%2Fjira%2Fcallback&state=7c3ad3ff-17b2-4c72-9c8b-401c9b201719&response_type=code&prompt=consent`