> DEVELOPER

I have been trying to modernize this app I can't build it because the PXSourceList. I am not sure what happened... maybe compare the main / master branch

> AGENT

I'll investigate the PXSourceList build issue by comparing your current branch against master.

> TOOL

tool_use Bash
id: toolu_01QBiT5qVe3fRPDR2bxb736U
```json
{
  "command": "git log --oneline master -15",
  "description": "Show recent commits on master branch"
}
```

> TOOL

tool_result
id: toolu_01QBiT5qVe3fRPDR2bxb736U
```
1053fe6 Bump build to 594
56eac5c Revert fix for Sidebar
db35975 Bump build to 593
351cddf Update credits file
128b80e Update sparkle framework
7f5c4b8 Fix deprecated API usages for 10.10
6ed3e41 Bump build to 592
ea470e2 Remove BumpBuild.sh
04ae12b Bump deployment target to 10.10
cc03f89 Bump build to 589
0d87fa7 Add substitute for +activateConstraints on 10.9
44ad7db Bump build to 588
31b6312 Don’t use qos queue attr maker on 10.9
69d20f1 Bump build to 587
5eed2d6 Stop shared instance alloc shenanigans
```

> TOOL

tool_use Bash
id: toolu_01Gu8gyw8qMmJ76VdwCaj763
```json
{
  "command": "git log --oneline modernize-macos26 -15",
  "description": "Show recent commits on current branch"
}
```

> TOOL

tool_result
id: toolu_01Gu8gyw8qMmJ76VdwCaj763
```
50117e5 Remove PXSourceList submodule
76c5ffd Remove Sparkle.framework and fix acknowledgements URL handling
1053fe6 Bump build to 594
56eac5c Revert fix for Sidebar
db35975 Bump build to 593
351cddf Update credits file
128b80e Update sparkle framework
7f5c4b8 Fix deprecated API usages for 10.10
6ed3e41 Bump build to 592
ea470e2 Remove BumpBuild.sh
04ae12b Bump deployment target to 10.10
cc03f89 Bump build to 589
0d87fa7 Add substitute for +activateConstraints on 10.9
44ad7db Bump build to 588
31b6312 Don’t use qos queue attr maker on 10.9
```

> TOOL

tool_use Bash
id: toolu_01RaiUHZfoPohz1GVcsBhJYy
```json
{
  "command": "grep -rn \"PXSourceList\" --include=\"*.pbxproj\" --include=\"*.h\" --include=\"*.m\" --include=\"*.swift\" . 2>/dev/null | head -50",
  "description": "Find PXSourceList references in source"
}
```

> TOOL

tool_result
id: toolu_01RaiUHZfoPohz1GVcsBhJYy
```
Cakebrew/Controllers/BPHomebrewViewController.h:23:#import <PXSourceList/PXSourceList.h>
Cakebrew/Controllers/BPSideBarController.m:14:@property (strong, nonatomic) PXSourceListItem *rootSidebarCategory;
Cakebrew/Controllers/BPSideBarController.m:16:@property (strong, nonatomic) PXSourceListItem *instaledFormulaeSidebarItem;
Cakebrew/Controllers/BPSideBarController.m:17:@property (strong, nonatomic) PXSourceListItem *outdatedFormulaeSidebarItem;
Cakebrew/Controllers/BPSideBarController.m:18:@property (strong, nonatomic) PXSourceListItem *allFormulaeSidebarItem;
Cakebrew/Controllers/BPSideBarController.m:19:@property (strong, nonatomic) PXSourceListItem *leavesFormulaeSidebarItem;
Cakebrew/Controllers/BPSideBarController.m:20:@property (strong, nonatomic) PXSourceListItem *repositoriesFormulaeSidebarItem;
Cakebrew/Controllers/BPSideBarController.m:37:	PXSourceListItem *item, *parent;
Cakebrew/Controllers/BPSideBarController.m:38:	_rootSidebarCategory = [PXSourceListItem itemWithTitle:@"" identifier:@"root"];
Cakebrew/Controllers/BPSideBarController.m:40:	parent = [PXSourceListItem itemWithTitle:NSLocalizedString(@"Sidebar_Group_Formulae", nil)
Cakebrew/Controllers/BPSideBarController.m:44:	_instaledFormulaeSidebarItem = [PXSourceListItem itemWithTitle:NSLocalizedString(@"Sidebar_Item_Installed", nil)
Cakebrew/Controllers/BPSideBarController.m:49:	_outdatedFormulaeSidebarItem = [PXSourceListItem itemWithTitle:NSLocalizedString(@"Sidebar_Item_Outdated", nil)
Cakebrew/Controllers/BPSideBarController.m:54:	_allFormulaeSidebarItem = [PXSourceListItem itemWithTitle:NSLocalizedString(@"Sidebar_Item_All", nil)
Cakebrew/Controllers/BPSideBarController.m:59:	_leavesFormulaeSidebarItem = [PXSourceListItem itemWithTitle:NSLocalizedString(@"Sidebar_Item_Leaves", nil)
Cakebrew/Controllers/BPSideBarController.m:64:	_repositoriesFormulaeSidebarItem = [PXSourceListItem itemWithTitle:NSLocalizedString(@"Sidebar_Item_Repos", nil)
Cakebrew/Controllers/BPSideBarController.m:69:	parent = [PXSourceListItem itemWithTitle:NSLocalizedString(@"Sidebar_Group_Tools", nil)
Cakebrew/Controllers/BPSideBarController.m:73:	item = [PXSourceListItem itemWithTitle:NSLocalizedString(@"Sidebar_Item_Doctor", nil)
Cakebrew/Controllers/BPSideBarController.m:79:	item = [PXSourceListItem itemWithTitle:NSLocalizedString(@"Sidebar_Item_Update", nil)
Cakebrew/Controllers/BPSideBarController.m:172:#pragma mark - PXSourceList Data Source
Cakebrew/Controllers/BPSideBarController.m:174:- (NSUInteger)sourceList:(PXSourceList*)sourceList numberOfChildrenOfItem:(id)item
Cakebrew/Controllers/BPSideBarController.m:179:		return [[(PXSourceListItem*)item children] count];
Cakebrew/Controllers/BPSideBarController.m:183:- (id)sourceList:(PXSourceList*)sourceList child:(NSUInteger)index ofItem:(id)item
Cakebrew/Controllers/BPSideBarController.m:188:		return [[(PXSourceListItem*)item children] objectAtIndex:index];
Cakebrew/Controllers/BPSideBarController.m:192:- (BOOL)sourceList:(PXSourceList*)sourceList isItemExpandable:(id)item
Cakebrew/Controllers/BPSideBarController.m:201:#pragma mark - PXSourceList Delegate
Cakebrew/Controllers/BPSideBarController.m:203:- (BOOL)sourceList:(PXSourceList *)aSourceList isGroupAlwaysExpanded:(id)group
Cakebrew/Controllers/BPSideBarController.m:208:- (NSView *)sourceList:(PXSourceList *)aSourceList viewForItem:(id)item
Cakebrew/Controllers/BPSideBarController.m:210:	PXSourceListTableCellView *cellView = nil;
Cakebrew/Controllers/BPSideBarController.m:212:	if ([[(PXSourceListItem*)item identifier] isEqualToString:@"group"]) {
Cakebrew/Controllers/BPSideBarController.m:218:	PXSourceListItem *sourceListItem = item;
Cakebrew/Controllers/BPSideBarController.h:9:@import PXSourceList;
Cakebrew/Controllers/BPSideBarController.h:29:@interface BPSideBarController : NSObject <PXSourceListDataSource, PXSourceListDelegate>
Cakebrew/Controllers/BPSideBarController.h:31:@property (assign) IBOutlet PXSourceList *sidebar;
Cakebrew.xcodeproj/project.pbxproj:27:		15A89D2B25F2C5F1003D33F5 /* PXSourceList.framework in Frameworks */ = {isa = PBXBuildFile; fileRef = 15A89D2A25F2C5F1003D33F5 /* PXSourceList.framework */; };
Cakebrew.xcodeproj/project.pbxproj:28:		15A89D2C25F2C5F1003D33F5 /* PXSourceList.framework in CopyFiles */ = {isa = PBXBuildFile; fileRef = […]

> AGENT

The branch has 2 commits beyond master. The last one removed the PXSourceList submodule, but the source code and Xcode project still reference it everywhere. Let me look at exactly what was removed.

> TOOL

tool_use Bash
id: toolu_01MRCqumPPX3UG9JtRDg9mKv
```json
{
  "command": "git show 50117e5 --stat",
  "description": "Show files changed in PXSourceList removal commit"
}
```

> TOOL

tool_result
id: toolu_01MRCqumPPX3UG9JtRDg9mKv
```
commit 50117e51e0508b4659c88b8acf5f62c11aa531aa
Author: Scott Densmore <<REDACTED_EMAIL>>
Date:   Sat Oct 18 16:45:58 2025 -0700

    Remove PXSourceList submodule

 .gitmodules               | 3 ---
 Dependencies/PXSourceList | 1 -
 2 files changed, 4 deletions(-)
```

> TOOL

tool_use Bash
id: toolu_016Yfo3z75mDoADZMrWK3RHh
```json
{
  "command": "cat .gitmodules 2>/dev/null; echo \"---- submodule status ----\"; git submodule status 2>/dev/null",
  "description": "Show gitmodules and submodule status"
}
```

> TOOL

tool_use Bash
id: toolu_01FWGbsfYgqnVP9pYhPLPh3H
```json
{
  "command": "git show master:.gitmodules 2>/dev/null; echo \"==== ls Frameworks dir current ====\"; ls -la Cakebrew/Frameworks/ 2>/dev/null; echo \"==== ls Frameworks on master ====\"; git ls-tree master -- Cakebrew/Frameworks/ 2>/dev/null; git ls-tree master 2>/dev/null | grep -i source",
  "description": "Compare submodule and frameworks layout vs master"
}
```

> TOOL

tool_result
id: toolu_016Yfo3z75mDoADZMrWK3RHh
```
---- submodule status ----
```

> TOOL

tool_result
id: toolu_01FWGbsfYgqnVP9pYhPLPh3H
```
[submodule "Dependencies/PXSourceList"]
	path = Dependencies/PXSourceList
	url = https://github.com/brunophilipe/PXSourceList.git
==== ls Frameworks dir current ====
total 16
drwxr-xr-x@  3 scottdensmore  staff    96 Oct 18  2025 .
drwxr-xr-x@ 47 scottdensmore  staff  1504 Oct 18  2025 ..
-rw-r--r--@  1 scottdensmore  staff  6148 Oct 18  2025 .DS_Store
==== ls Frameworks on master ====
040000 tree 7b1f4427ce10766c1b1f136f8eb1bf6268432ba2	Cakebrew/Frameworks/Sparkle.framework
```

> TOOL

tool_use Bash
id: toolu_01VgXdH3f4rzvDfwioT429m3
```json
{
  "command": "ls -la Dependencies/ 2>/dev/null; echo \"==== git ls-tree master Dependencies ====\"; git ls-tree master -- Dependencies/ 2>/dev/null; echo \"==== current HEAD Dependencies ====\"; git ls-tree HEAD -- Dependencies/ 2>/dev/null",
  "description": "Inspect Dependencies dir on disk and in git"
}
```

> TOOL

tool_result
id: toolu_01VgXdH3f4rzvDfwioT429m3
```
total 16
drwxr-xr-x@  3 scottdensmore  staff    96 Oct 18  2025 .
drwxr-xr-x@ 16 scottdensmore  staff   512 May 25 15:38 ..
-rw-r--r--@  1 scottdensmore  staff  6148 Oct 18  2025 .DS_Store
==== git ls-tree master Dependencies ====
160000 commit 38cecbd7e1d8449cac2db4ed03fb0dd3cee14f9f	Dependencies/PXSourceList
==== current HEAD Dependencies ====
```

> TOOL

tool_use Bash
id: toolu_01J9qjVc9JyVYsPLBJn6vcLs
```json
{
  "command": "git diff master..HEAD --stat",
  "description": "Show all files changed between master and current branch"
}
```

> TOOL

tool_result
id: toolu_01J9qjVc9JyVYsPLBJn6vcLs
```
 .genkit/traces_idx/genkit.metadata                 |    1 +
 .gitmodules                                        |    3 -
 Cakebrew.xcodeproj/project.pbxproj                 |   91 +-
 .../xcshareddata/xcschemes/Cakebrew.xcscheme       |    2 +-
 .../xcshareddata/xcschemes/CakebrewTests.xcscheme  |    2 +-
 Cakebrew/BPAppDelegate.m                           |   54 +-
 Cakebrew/BPFormulaeTableView.m                     |    2 +-
 Cakebrew/BPHomebrewManager.m                       |   28 +-
 Cakebrew/BPToolbar.m                               |    6 +-
 Cakebrew/Base.lproj/MainMenu.xib                   |   32 +-
 Cakebrew/Controllers/BPSideBarController.m         |    2 -
 Cakebrew/Frameworks/Sparkle.framework/Headers      |    1 -
 Cakebrew/Frameworks/Sparkle.framework/Modules      |    1 -
 .../Frameworks/Sparkle.framework/PrivateHeaders    |    1 -
 Cakebrew/Frameworks/Sparkle.framework/Resources    |    1 -
 Cakebrew/Frameworks/Sparkle.framework/Sparkle      |    1 -
 .../Versions/A/Headers/SPUDownloadData.h           |   43 -
 .../Versions/A/Headers/SPUDownloader.h             |   25 -
 .../Versions/A/Headers/SPUDownloaderDelegate.h     |   38 -
 .../Versions/A/Headers/SPUDownloaderProtocol.h     |   34 -
 .../Versions/A/Headers/SPUDownloaderSession.h      |   20 -
 .../Versions/A/Headers/SPUURLRequest.h             |   35 -
 .../Versions/A/Headers/SUAppcast.h                 |   31 -
 .../Versions/A/Headers/SUAppcastItem.h             |   55 -
 .../Versions/A/Headers/SUCodeSigningVerifier.h     |   26 -
 .../Versions/A/Headers/SUErrors.h                  |   58 -
 .../Versions/A/Headers/SUExport.h                  |   18 -
 .../A/Headers/SUStandardVersionComparator.h        |   52 -
 .../Versions/A/Headers/SUUpdater.h                 |  233 --
 .../Versions/A/Headers/SUUpdaterDelegate.h         |  352 --
 .../A/Headers/SUVersionComparisonProtocol.h        |   37 -
 .../Versions/A/Headers/SUVersionDisplayProtocol.h  |   29 -
 .../Sparkle.framework/Versions/A/Headers/Sparkle.h |   38 -
 .../Versions/A/Modules/module.modulemap            |    6 -
 .../Versions/A/PrivateHeaders/SUUnarchiver.h       |   21 -
 .../A/Resources/Autoupdate.app/Contents/Info.plist |   56 -
 .../Autoupdate.app/Contents/MacOS/Autoupdate       |  Bin 545056 -> 0 bytes
 .../Resources/Autoupdate.app/Contents/MacOS/fileop |  Bin 286720 -> 0 bytes
 .../A/Resources/Autoupdate.app/Contents/PkgInfo    |    1 -
 .../Autoupdate.app/Contents/Resources/AppIcon.icns |  Bin 37132 -> 0 bytes
 .../Contents/Resources/Base.lproj/Sparkle.strings  |  Bin 10196 -> 0 bytes
 .../Autoupdate.app/Contents/Resources/SUStatus.nib |  Bin 12712 -> 0 bytes
 .../Contents/Resources/ar.lproj/Sparkle.strings    |  Bin 8468 -> 0 bytes
 .../Contents/Resources/ca.lproj/Sparkle.strings    |  Bin 6792 -> 0 […]

> AGENT

I now understand what happened. Let me read the actual sidebar code to assess the migration scope.

> TOOL

tool_use Read
id: toolu_01WdWzjJ6hN97qihf55ck7AK
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/Controllers/BPSideBarController.m"
}
```

> TOOL

tool_result
id: toolu_01WdWzjJ6hN97qihf55ck7AK
```
1	//
2	//  BPSideBarController.m
3	//  Cakebrew
4	//
5	//  Created by Marek Hrusovsky on 05/09/14.
6	//  Copyright (c) 2014 Bruno Philipe. All rights reserved.
7	//
8	
9	#import "BPSideBarController.h"
10	#import "BPHomebrewManager.h"
11	
12	@interface BPSideBarController()
13	
14	@property (strong, nonatomic) PXSourceListItem *rootSidebarCategory;
15	
16	@property (strong, nonatomic) PXSourceListItem *instaledFormulaeSidebarItem;
17	@property (strong, nonatomic) PXSourceListItem *outdatedFormulaeSidebarItem;
18	@property (strong, nonatomic) PXSourceListItem *allFormulaeSidebarItem;
19	@property (strong, nonatomic) PXSourceListItem *leavesFormulaeSidebarItem;
20	@property (strong, nonatomic) PXSourceListItem *repositoriesFormulaeSidebarItem;
21	
22	@end
23	
24	@implementation BPSideBarController
25	
26	- (instancetype)init
27	{
28		self = [super init];
29		if (self) {
30			[self buildSidebarTree];
31		}
32		return self;
33	}
34	
35	- (void)buildSidebarTree
36	{
37		PXSourceListItem *item, *parent;
38		_rootSidebarCategory = [PXSourceListItem itemWithTitle:@"" identifier:@"root"];
39		
40		parent = [PXSourceListItem itemWithTitle:NSLocalizedString(@"Sidebar_Group_Formulae", nil)
41									  identifier:@"group"];
42		[_rootSidebarCategory addChildItem:parent];
43		
44		_instaledFormulaeSidebarItem = [PXSourceListItem itemWithTitle:NSLocalizedString(@"Sidebar_Item_Installed", nil)
45															identifier:@"item"];
46		_instaledFormulaeSidebarItem.icon = [self installedSidebarIconImage];
47		[parent addChildItem:_instaledFormulaeSidebarItem];
48		
49		_outdatedFormulaeSidebarItem = [PXSourceListItem itemWithTitle:NSLocalizedString(@"Sidebar_Item_Outdated", nil)
50															identifier:@"item"];
51		_outdatedFormulaeSidebarItem.icon = [self outdatedSidebarIconImage];
52		[parent addChildItem:_outdatedFormulaeSidebarItem];
53		
54		_allFormulaeSidebarItem = [PXSourceListItem itemWithTitle:NSLocalizedString(@"Sidebar_Item_All", nil)
55													   identifier:@"item"];
56		_allFormulaeSidebarItem.icon = [self allFormulaeSidebarIconImage];
57		[parent addChildItem:_allFormulaeSidebarItem];
58		
59		_leavesFormulaeSidebarItem = [PXSourceListItem itemWithTitle:NSLocalizedString(@"Sidebar_Item_Leaves", […]

> TOOL

tool_use Read
id: toolu_01YSFjowuiq5ykCtTVUvjEDL
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/Controllers/BPSideBarController.h"
}
```

> TOOL

tool_result
id: toolu_01YSFjowuiq5ykCtTVUvjEDL
```
1	//
2	//  BPSideBarController.h
3	//  Cakebrew
4	//
5	//  Created by Marek Hrusovsky on 05/09/14.
6	//  Copyright (c) 2014 Bruno Philipe. All rights reserved.
7	//
8	
9	@import PXSourceList;
10	@import Foundation;
11	
12	typedef NS_ENUM(NSUInteger, FormulaeSideBarItem)
13	{
14		FormulaeSideBarItemFormulaeCategory = 0,
15		FormulaeSideBarItemInstalled = 1,
16		FormulaeSideBarItemOutdated = 2,
17		FormulaeSideBarItemAll = 3,
18		FormulaeSideBarItemLeaves = 4,
19		FormulaeSideBarItemRepositories = 5,
20		FormulaeSideBarItemToolsCategory = 6,
21		FormulaeSideBarItemDoctor = 7,
22		FormulaeSideBarItemUpdate = 8,
23	};
24	
25	@protocol BPSideBarControllerDelegate <NSObject>
26	- (void)sourceListSelectionDidChange;
27	@end
28	
29	@interface BPSideBarController : NSObject <PXSourceListDataSource, PXSourceListDelegate>
30	
31	@property (assign) IBOutlet PXSourceList *sidebar;
32	
33	@property (weak) id <BPSideBarControllerDelegate>delegate;
34	
35	- (void)refreshSidebarBadges;
36	- (void)configureSidebarSettings;
37	
38	- (IBAction)selectSideBarRowWithSenderTag:(id)sender;
39	
40	@end
41	
```

> TOOL

tool_use Read
id: toolu_01REmB72ThnzyXBoHdwcRsYS
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/Controllers/BPHomebrewViewController.h"
}
```

> TOOL

tool_result
id: toolu_01REmB72ThnzyXBoHdwcRsYS
```
1	//
2	//	HomebrewController.h
3	//	Cakebrew – The Homebrew GUI App for OS X
4	//
5	//	Created by Vincent Saluzzo on 06/12/11.
6	//	Copyright (c) 2014 Bruno Philipe. All rights reserved.
7	//
8	//	This program is free software: you can redistribute it and/or modify
9	//	it under the terms of the GNU General Public License as published by
10	//	the Free Software Foundation, either version 3 of the License, or
11	//	(at your option) any later version.
12	//
13	//	This program is distributed in the hope that it will be useful,
14	//	but WITHOUT ANY WARRANTY; without even the implied warranty of
15	//	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
16	//	GNU General Public License for more details.
17	//
18	//	You should have received a copy of the GNU General Public License
19	//	along with this program.  If not, see <http://www.gnu.org/licenses/>.
20	//
21	
22	#import <Foundation/Foundation.h>
23	#import <PXSourceList/PXSourceList.h>
24	#import "BPFormula.h"
25	#import "BPFormulaeTableView.h"
26	#import "BPFormulaPopoverViewController.h"
27	#import "BPSideBarController.h"
28	
29	typedef NS_ENUM(NSUInteger, BPWindowOperation) {
30		kBPWindowOperationInstall,
31		kBPWindowOperationUninstall,
32		kBPWindowOperationUpgrade,
33		kBPWindowOperationTap, […]

> AGENT

Let me check the remaining PXSourceList touchpoints — the XIB and the view controller implementation — to size the fix accurately.

> TOOL

tool_use Bash
id: toolu_01FVdC2XuHzJ7dY8YbQB5DXE
```json
{
  "command": "grep -n \"PXSourceList\\|badgeView\\|BPBadge\\|sourceList\" Cakebrew/Base.lproj/MainMenu.xib | head -40",
  "description": "Find PXSourceList usage in the XIB"
}
```

> TOOL

tool_result
id: toolu_01FVdC2XuHzJ7dY8YbQB5DXE
```
952:                    <outlineView verticalHuggingPriority="750" allowsExpansionToolTips="YES" columnAutoresizingStyle="lastColumnOnly" selectionHighlightStyle="sourceList" columnReordering="NO" multipleSelection="NO" autosaveColumns="NO" rowHeight="32" rowSizeStyle="systemDefault" viewBased="YES" indentationPerLevel="13" outlineTableColumn="Dme-LE-cyv" id="9f4-xo-e1c" customClass="PXSourceList">
955:                        <color key="backgroundColor" name="_sourceListBackgroundColor" catalog="System" colorSpace="catalog"/>
970:                                    <tableCellView identifier="HeaderCell" id="266-1g-zfm" customClass="PXSourceListTableCellView">
988:                                    <tableCellView identifier="MainCell" id="Emw-wX-GZR" customClass="PXSourceListTableCellView">
1011:                                                    <customView horizontalHuggingPriority="252" verticalHuggingPriority="751" horizontalCompressionResistancePriority="780" verticalCompressionResistancePriority="780" placeholderIntrinsicWidth="40" placeholderIntrinsicHeight="16" translatesAutoresizingMaskIntoConstraints="NO" id="NXZ-4S-anG" customClass="PXSourceListBadgeView">
1034:                                            <outlet property="badgeView" destination="NXZ-4S-anG" id="cnN-Fx-bd2"/>
```

> TOOL

tool_use Bash
id: toolu_01VZnHp4LpqaLPEDfMiw6UB6
```json
{
  "command": "grep -rn \"PXSourceList\\|badgeView\\|BadgeCell\\|MainCell\\|HeaderCell\" Cakebrew/Controllers/BPHomebrewViewController.m 2>/dev/null | head; echo \"==== badge class files ====\"; grep -rln \"badgeView\\|PXSourceListBadge\\|Badge\" Cakebrew --include=*.h --include=*.m | head",
  "description": "Find PXSourceList and badge usage in view controller and badge classes"
}
```

> TOOL

tool_result
id: toolu_01VZnHp4LpqaLPEDfMiw6UB6
```
==== badge class files ====
(eval):1: no matches found: --include=*.h
```

> AGENT

## What happened

On `modernize-macos26` you have two commits past `master`:
- `76c5ffd` — removed Sparkle.framework
- `50117e5` — **removed the `Dependencies/PXSourceList` git submodule** (deleted the submodule entry and the `.gitmodules` line)

That last commit pulled out the library but nothing replaced it, and the app still depends on PXSourceList in three places, so the build can't resolve it:

1. **Source code** — the whole sidebar is built on it:
   - [BPSideBarController.h](Cakebrew/Controllers/BPSideBarController.h) — `@import PXSourceList;`, conforms to `PXSourceListDataSource`/`PXSourceListDelegate`, `IBOutlet PXSourceList *sidebar`
   - [BPSideBarController.m](Cakebrew/Controllers/BPSideBarController.m) — uses `PXSourceListItem`, `PXSourceListTableCellView` throughout
   - [BPHomebrewViewController.h:23](Cakebrew/Controllers/BPHomebrewViewController.h:23) — `#import <PXSourceList/PXSourceList.h>`
2. **Xcode project** — [project.pbxproj](Cakebrew.xcodeproj/project.pbxproj) still links & copies `PXSourceList.framework` and sets `USER_HEADER_SEARCH_PATHS` to its headers. The framework was built from the submodule, which is now gone.
3. **The XIB** — [MainMenu.xib:952](Cakebrew/Base.lproj/MainMenu.xib:952) sets the sidebar's `customClass="PXSourceList"`, with cells `PXSourceListTableCellView` and a `PXSourceListBadgeView`.

So this wasn't an accident in the usual sense — the submodule was deliberately removed, but the migration off PXSourceList was never done.

## Two ways forward

The good news: PXSourceList is just an old wrapper around `NSOutlineView` to get the "source list" sidebar look. Modern AppKit does that natively — your XIB already has `selectionHighlightStyle="sourceList"` and a `_sourceListBackgroundColor`. So you don't need the library […]

> TOOL

tool_use AskUserQuestion
id: toolu_01SkqWbvxvFS4K6hLFc7vRS9
```json
{
  "questions": [
    {
      "question": "How do you want to resolve the PXSourceList build break?",
      "header": "Approach",
      "multiSelect": false,
      "options": [
        {
          "label": "Migrate to native NSOutlineView",
          "description": "Rewrite the sidebar on plain NSOutlineView (source-list style) and remove PXSourceList from code, project, and XIB. The real 'modernize' end-state, but touches the XIB and badge view. Larger change."
        },
        {
          "label": "Restore the submodule to unblock",
          "description": "Revert commit 50117e5, re-init the PXSourceList submodule so it builds again now. Fast, but keeps an old dependency that may not build cleanly on the latest Xcode/SDK."
        },
        {
          "label": "Just diagnose for now",
          "description": "Stop here — I've explained what broke. You'll decide later."
        }
      ]
    }
  ]
}
```

> TOOL

tool_result
id: toolu_01SkqWbvxvFS4K6hLFc7vRS9
```
Your questions have been answered: "How do you want to resolve the PXSourceList build break?"="Migrate to native NSOutlineView". You can now continue with these answers in mind.
```

> AGENT

I'll migrate the sidebar to a native `NSOutlineView`. Let me gather the full context first — the XIB sidebar structure, how the view controller uses the sidebar, and the project's framework references.

> TOOL

tool_use Read
id: toolu_01EC1BPkc75p6RJy61YR5qZi
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/Base.lproj/MainMenu.xib",
  "offset": 940,
  "limit": 110
}
```

> TOOL

tool_result
id: toolu_01EC1BPkc75p6RJy61YR5qZi
```
940	                <constraint firstItem="08Y-7c-3Hu" firstAttribute="leading" secondItem="du9-Lg-Fwn" secondAttribute="leading" id="xj2-O2-zSU"/>
941	                <constraint firstAttribute="trailing" secondItem="lYz-uI-q1s" secondAttribute="trailing" id="yEW-SB-Mx4"/>
942	            </constraints>
943	            <point key="canvasLocation" x="118" y="-308.5"/>
944	        </customView>
945	        <scrollView borderType="none" autohidesScrollers="YES" horizontalLineScroll="32" horizontalPageScroll="10" verticalLineScroll="32" verticalPageScroll="10" usesPredominantAxisScrolling="NO" horizontalScrollElasticity="none" verticalScrollElasticity="none" id="bme-rl-6Ta">
946	            <rect key="frame" x="0.0" y="0.0" width="210" height="275"/>
947	            <autoresizingMask key="autoresizingMask" flexibleMaxX="YES" flexibleMinY="YES"/>
948	            <clipView key="contentView" drawsBackground="NO" id="xPi-so-Sop">
949	                <rect key="frame" x="0.0" y="0.0" width="210" height="275"/>
950	                <autoresizingMask key="autoresizingMask"/>
951	                <subviews>
952	                    <outlineView verticalHuggingPriority="750" allowsExpansionToolTips="YES" columnAutoresizingStyle="lastColumnOnly" selectionHighlightStyle="sourceList" columnReordering="NO" multipleSelection="NO" autosaveColumns="NO" rowHeight="32" rowSizeStyle="systemDefault" viewBased="YES" indentationPerLevel="13" outlineTableColumn="Dme-LE-cyv" id="9f4-xo-e1c" customClass="PXSourceList">
953	                        <rect key="frame" x="0.0" y="0.0" width="210" height="275"/>
954	                        <autoresizingMask key="autoresizingMask" widthSizable="YES" heightSizable="YES"/>
955	                        <color key="backgroundColor" name="_sourceListBackgroundColor" catalog="System" colorSpace="catalog"/>
956	                        <color key="gridColor" name="gridColor" catalog="System" colorSpace="catalog"/>
957	                        <tableColumns>
958	                            <tableColumn identifier="AutomaticTableColumnIdentifier.0" width="178" minWidth="16" maxWidth="1000" id="Dme-LE-cyv">
959	                                <tableHeaderCell key="headerCell" lineBreakMode="truncatingTail" borderStyle="border" alignment="left">
960	                                    <color key="textColor" name="headerTextColor" catalog="System" colorSpace="catalog"/>
961	                                    <color key="backgroundColor" white="0.33333298560000002" alpha="1" colorSpace="calibratedWhite"/>
962	                                </tableHeaderCell>
963	                                <textFieldCell key="dataCell" lineBreakMode="truncatingTail" selectable="YES" editable="YES" alignment="left" title="Text Cell" id="bOO-GN-auw">
964	                                    <font key="font" metaFont="system"/>
965	                                    <color key="textColor" name="controlTextColor" catalog="System" colorSpace="catalog"/>
966	                                    <color key="backgroundColor" name="controlBackgroundColor" catalog="System" colorSpace="catalog"/>
967	                                </textFieldCell>
968	                                <tableColumnResizingMask key="resizingMask" resizeWithTable="YES" userResizable="YES"/>
969	                                <prototypeCellViews>
970	                                    <tableCellView identifier="HeaderCell" id="266-1g-zfm" customClass="PXSourceListTableCellView">
971	                                        <rect key="frame" x="10" y="0.0" width="190" height="17"/>
972	                                        <autoresizingMask key="autoresizingMask" widthSizable="YES" heightSizable="YES"/>
973	                                        <subviews>
974	                                            <textField focusRingType="none" verticalHuggingPriority="750" fixedFrame="YES" translatesAutoresizingMaskIntoConstraints="NO" id="zqu-hn-vHh">
975	                                                <rect key="frame" […]

> TOOL

tool_use Bash
id: toolu_01WbuR17JiLb1PEp4zE2cRKa
```json
{
  "command": "grep -n \"sidebar\\|sourceList\\|SideBar\\|outlineView\\|selectRow\\|selectedRow\\|itemAtRow\\|rowForItem\\|reloadData\\|FormulaeSideBarItem\" Cakebrew/Controllers/BPHomebrewViewController.m | head -60",
  "description": "Find sidebar interactions in view controller"
}
```

> TOOL

tool_result
id: toolu_01WbuR17JiLb1PEp4zE2cRKa
```
49:BPSideBarControllerDelegate,
196:	[self.sidebarController setDelegate:self];
197:	[self.sidebarController refreshSidebarBadges];
198:	[self.sidebarController configureSidebarSettings];
291:	NSInteger selectedSidebarRow	= [self.sidebarController.sidebar selectedRow];
292:	NSInteger selectedIndex			= [self.formulaeTableView selectedRow];
293:	NSIndexSet *selectedRows		= [self.formulaeTableView selectedRowIndexes];
294:	NSArray *selectedFormulae		= [self.formulaeDataSource formulasAtIndexSet:selectedRows];
303:	if (selectedSidebarRow == FormulaeSideBarItemRepositories) // Repositories (Taps) sidebaritem
316:	else if (selectedIndex == -1 || selectedSidebarRow > FormulaeSideBarItemToolsCategory)
320:	else if ([[self.formulaeTableView selectedRowIndexes] count] > 1)
334:				if (selectedSidebarRow == FormulaeSideBarItemOutdated) {
363:	[self.formulaeTableView reloadData];
372:	FormulaeSideBarItem selectedSidebarRow = [self.sidebarController.sidebar selectedRow];
383:			case FormulaeSideBarItemInstalled: // Installed Formulae
387:			case FormulaeSideBarItemOutdated: // Outdated Formulae
391:			case FormulaeSideBarItemAll: // All Formulae
395:			case FormulaeSideBarItemLeaves:	// Leaves
399:			case FormulaeSideBarItemRepositories: // Repositories
403:			case FormulaeSideBarItemDoctor: // Doctor
407:			case FormulaeSideBarItemUpdate: // Update Tool
449:		BOOL shouldReselectFirstRow = ([self.sidebarController.sidebar selectedRow] < 0);
451:		[self.sidebarController refreshSidebarBadges];
452:		[self.sidebarController.sidebar reloadData];
457:			[self.sidebarController.sidebar selectRowIndexes:[NSIndexSet indexSetWithIndex:FormulaeSideBarItemInstalled] byExtendingSelection:NO];
459:			[self.sidebarController.sidebar selectRowIndexes:[NSIndexSet indexSetWithIndex:(NSUInteger)_lastSelectedSidebarIndex] byExtendingSelection:NO];
522:	NSInteger selectedIndex = [self.formulaeTableView selectedRow];
545:	[self.sidebarController.sidebar selectRowIndexes:[NSIndexSet indexSetWithIndex:FormulaeSideBarItemAll]
573:#pragma mark - BPSideBarDelegate Delegate
575:- (void)sourceListSelectionDidChange
578:	NSInteger selectedSidebarRow = [self.sidebarController.sidebar selectedRow];
594:		case FormulaeSideBarItemInstalled: // Installed Formulae
598:		case FormulaeSideBarItemOutdated: // Outdated Formulae
602:		case FormulaeSideBarItemAll: // All Formulae
606:		case FormulaeSideBarItemLeaves:	// Leaves
610:		case FormulaeSideBarItemRepositories: // Repositories
614:		case FormulaeSideBarItemDoctor: // Doctor
618: […]

> AGENT

This is very helpful — the row-index selection in the view controller maps directly to a flat, fully-expanded outline, so an `NSOutlineView` with both groups expanded preserves the existing `FormulaeSideBarItem` numbering. Now let me examine the project file references and confirm there are no other PXSourceList touchpoints.

> TOOL

tool_use Bash
id: toolu_01R1ovFF9szKZL5mSBNU4iM6
```json
{
  "command": "grep -n \"PXSourceList\\|ContainerItemProxy\\|TargetDependency\\|PBXReferenceProxy\\|ProductsGroup\\|\\.xcodeproj\\|Dependencies\" Cakebrew.xcodeproj/project.pbxproj",
  "description": "Find all PXSourceList and project-reference entries in pbxproj"
}
```

> TOOL

tool_result
id: toolu_01R1ovFF9szKZL5mSBNU4iM6
```
27:		15A89D2B25F2C5F1003D33F5 /* PXSourceList.framework in Frameworks */ = {isa = PBXBuildFile; fileRef = 15A89D2A25F2C5F1003D33F5 /* PXSourceList.framework */; };
28:		15A89D2C25F2C5F1003D33F5 /* PXSourceList.framework in CopyFiles */ = {isa = PBXBuildFile; fileRef = 15A89D2A25F2C5F1003D33F5 /* PXSourceList.framework */; settings = {ATTRIBUTES = (CodeSignOnCopy, RemoveHeadersOnCopy, ); }; };
100:				15A89D2C25F2C5F1003D33F5 /* PXSourceList.framework in CopyFiles */,
165:		15A89D2A25F2C5F1003D33F5 /* PXSourceList.framework */ = {isa = PBXFileReference; explicitFileType = wrapper.framework; path = PXSourceList.framework; sourceTree = BUILT_PRODUCTS_DIR; };
292:				15A89D2B25F2C5F1003D33F5 /* PXSourceList.framework in Frameworks */,
454:				15A89D2A25F2C5F1003D33F5 /* PXSourceList.framework */,
1050:				USER_HEADER_SEARCH_PATHS = "$(PROJECT_DIR)/Cakebrew/Frameworks/PXSourceList.framework/Headers";
1087:				USER_HEADER_SEARCH_PATHS = "$(PROJECT_DIR)/Cakebrew/Frameworks/PXSourceList.framework/Headers";
```

> TOOL

tool_use Bash
id: toolu_01P4g6aKcf96tydYqp6XB64h
```json
{
  "command": "echo \"==== other xibs/storyboards referencing PX ====\"; grep -rln \"PXSourceList\\|PXSourceListBadge\" Cakebrew --include=*.xib --include=*.storyboard 2>/dev/null; echo \"==== sidebar outlet connection in xib ====\"; grep -n \"property=\\\"sidebar\\\"\\|property=\\\"sidebarController\\\"\\|customClass=\\\"BPSideBarController\\\"\\|id=\\\"SGP-Ky-0Th\\\"\" Cakebrew/Base.lproj/MainMenu.xib; echo \"==== any PX in whole repo (non-git) ====\"; grep -rn \"PXSourceList\" Cakebrew CakebrewTests 2>/dev/null | grep -v \"\\.xib:\" | grep -v \"BPSideBarController\\|BPHomebrewViewController\"",
  "description": "Check other xibs and sidebar outlet wiring"
}
```

> TOOL

tool_result
id: toolu_01P4g6aKcf96tydYqp6XB64h
```
==== other xibs/storyboards referencing PX ====
(eval):1: no matches found: --include=*.xib
```

> TOOL

tool_use Bash
id: toolu_01WHVEbgVr1Q2AGZPPqR4bxp
```json
{
  "command": "echo \"==== workspace? ====\"; ls -la *.xcworkspace 2>/dev/null; find . -name \"*.xcworkspace\" -not -path \"*/xcuserdata/*\" 2>/dev/null; echo \"==== other xibs referencing PX ====\"; grep -rln \"PXSourceList\" Cakebrew --include=\"*.xib\" --include=\"*.storyboard\" 2>/dev/null; echo \"==== sidebar wiring in MainMenu.xib ====\"; grep -n \"sidebar\\|sidebarController\\|BPSideBarController\\|SGP-Ky-0Th\" Cakebrew/Base.lproj/MainMenu.xib",
  "description": "Check for workspace and sidebar outlet wiring"
}
```

> TOOL

tool_result
id: toolu_01WHVEbgVr1Q2AGZPPqR4bxp
```
==== workspace? ====
total 8
drwxr-xr-x@  5 scottdensmore  staff  160 Oct 18  2025 .
drwxr-xr-x@ 16 scottdensmore  staff  512 May 25 15:38 ..
-rw-r--r--@  1 scottdensmore  staff  259 Oct  2  2022 contents.xcworkspacedata
drwxr-xr-x@  4 scottdensmore  staff  128 Oct 18  2025 xcshareddata
drwxr-xr-x   3 scottdensmore  staff   96 Oct 18  2025 xcuserdata
./Cakebrew.xcworkspace
./Cakebrew.xcodeproj/project.xcworkspace
==== other xibs referencing PX ====
Cakebrew/Base.lproj/MainMenu.xib
==== sidebar wiring in MainMenu.xib ====
495:                                    <action selector="selectSideBarRowWithSenderTag:" target="SGP-Ky-0Th" id="Cet-wG-7MQ"/>
501:                                    <action selector="selectSideBarRowWithSenderTag:" target="SGP-Ky-0Th" id="c5K-Fg-jvj"/>
507:                                    <action selector="selectSideBarRowWithSenderTag:" target="SGP-Ky-0Th" id="opC-R1-TQR"/>
513:                                    <action selector="selectSideBarRowWithSenderTag:" target="SGP-Ky-0Th" id="Uhl-lk-qPT"/>
519:                                    <action selector="selectSideBarRowWithSenderTag:" target="SGP-Ky-0Th" id="s3g-8g-eFB"/>
526:                                    <action selector="selectSideBarRowWithSenderTag:" target="SGP-Ky-0Th" id="DMG-th-yEC"/>
532:                                    <action selector="selectSideBarRowWithSenderTag:" target="SGP-Ky-0Th" id="fUp-dE-WjG"/>
740:        <customObject id="SGP-Ky-0Th" customClass="BPSideBarController">
743:                <outlet property="sidebar" destination="9f4-xo-e1c" id="4QJ-Bv-GMs"/>
756:                <outlet property="sidebarController" destination="SGP-Ky-0Th" id="etb-bD-RB5"/>
763:                <outlet property="sidebarView" destination="bme-rl-6Ta" id="BLl-fS-pI6"/>
1043:                            <outlet property="dataSource" destination="SGP-Ky-0Th" id="Bp4-h7-9E9"/>
1044:                            <outlet property="delegate" destination="SGP-Ky-0Th" id="dNS-Xe-zJ9"/>
```

> TOOL

tool_use Read
id: toolu_014cN8yMRT3hEJSmVZovgBwg
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcworkspace/contents.xcworkspacedata"
}
```

> TOOL

tool_result
id: toolu_014cN8yMRT3hEJSmVZovgBwg
```
1	<?xml version="1.0" encoding="UTF-8"?>
2	<Workspace
3	   version = "1.0">
4	   <FileRef
5	      location = "container:Cakebrew.xcodeproj">
6	   </FileRef>
7	   <FileRef
8	      location = "group:Dependencies/PXSourceList/PXSourceList.xcodeproj">
9	   </FileRef>
10	</Workspace>
11	
```

> AGENT

Found it — the workspace [contents.xcworkspacedata:7](Cakebrew.xcworkspace/contents.xcworkspacedata:7) still references the deleted `Dependencies/PXSourceList/PXSourceList.xcodeproj`. That's the root build failure alongside the project's framework links. Let me read the exact pbxproj regions I need to edit.

> TOOL

tool_use Read
id: toolu_01Sp8eEGXAkoRdByPq2mepp7
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcodeproj/project.pbxproj",
  "offset": 20,
  "limit": 14
}
```

> TOOL

tool_result
id: toolu_01Sp8eEGXAkoRdByPq2mepp7
```
20			1570BA3618EE0A66001C3C5C /* BPHomebrewManager.m in Sources */ = {isa = PBXBuildFile; fileRef = 1570BA3518EE0A66001C3C5C /* BPHomebrewManager.m */; };
21			1570BA5618EE50BD001C3C5C /* BPFormula.m in Sources */ = {isa = PBXBuildFile; fileRef = 1570BA5518EE50BD001C3C5C /* BPFormula.m */; };
22			15715F611C78050B00AE0E66 /* BPBundleWindow.xib in Resources */ = {isa = PBXBuildFile; fileRef = 15715F5F1C78050B00AE0E66 /* BPBundleWindow.xib */; };
23			15715F641C78053300AE0E66 /* BPBundleWindowController.m in Sources */ = {isa = PBXBuildFile; fileRef = 15715F631C78053300AE0E66 /* BPBundleWindowController.m */; };
24			1584884A1F0708F000BD2CD9 /* brewinfo_nmap.txt in Resources */ = {isa = PBXBuildFile; fileRef = 158488491F0708F000BD2CD9 /* brewinfo_nmap.txt */; };
25			1594D13C1B8A6D1A00F764FA /* QuartzCore.framework in Frameworks */ = {isa = PBXBuildFile; fileRef = 15D2CFAC18F202D000B6D9F1 /* QuartzCore.framework */; };
26			15A00B411B8406FB00528486 /* Credits.rtf in Resources */ = {isa = PBXBuildFile; fileRef = 15A00B401B8406FB00528486 /* Credits.rtf */; };
27			15A89D2B25F2C5F1003D33F5 /* PXSourceList.framework in Frameworks */ = {isa = PBXBuildFile; fileRef = 15A89D2A25F2C5F1003D33F5 /* PXSourceList.framework */; };
28			15A89D2C25F2C5F1003D33F5 /* PXSourceList.framework in CopyFiles */ = {isa = PBXBuildFile; fileRef = 15A89D2A25F2C5F1003D33F5 /* PXSourceList.framework */; settings = {ATTRIBUTES = (CodeSignOnCopy, RemoveHeadersOnCopy, ); }; };
29			15A89D3925F2F467003D33F5 /* NSLayoutConstraint+Shims.m in Sources */ = {isa = PBXBuildFile; fileRef = 15A89D3825F2F467003D33F5 /* NSLayoutConstraint+Shims.m */; };
30			15B23A2C18F5003600714212 /* dsa_pub.pem in Resources */ = […]

> TOOL

tool_use Read
id: toolu_01DKwo4XBtKADq5pBUDGP2GY
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcodeproj/project.pbxproj",
  "offset": 93,
  "limit": 15
}
```

> TOOL

tool_result
id: toolu_01DKwo4XBtKADq5pBUDGP2GY
```
93	/* Begin PBXCopyFilesBuildPhase section */
94			1570BA6018EF9B0F001C3C5C /* CopyFiles */ = {
95				isa = PBXCopyFilesBuildPhase;
96				buildActionMask = 2147483647;
97				dstPath = "";
98				dstSubfolderSpec = 10;
99				files = (
100					15A89D2C25F2C5F1003D33F5 /* PXSourceList.framework in CopyFiles */,
101				);
102				runOnlyForDeploymentPostprocessing = 0;
103			};
104	/* End PBXCopyFilesBuildPhase section */
105	
106	/* Begin PBXFileReference section */
107			150AEC381B3F999A00163767 /* BPDoctorViewController.h */ = {isa = PBXFileReference; fileEncoding = 4; lastKnownFileType = sourcecode.c.h; name = BPDoctorViewController.h; path = Controllers/BPDoctorViewController.h; sourceTree = "<group>"; };
```

> TOOL

tool_use Read
id: toolu_01N7FvUKAt1agCyYB39K4eum
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcodeproj/project.pbxproj",
  "offset": 285,
  "limit": 12
}
```

> TOOL

tool_result
id: toolu_01N7FvUKAt1agCyYB39K4eum
```
285			1FE4FE51148E4CDD008EDE8B /* Frameworks */ = {
286				isa = PBXFrameworksBuildPhase;
287				buildActionMask = 2147483647;
288				files = (
289					D2CC8CA71B90F04C00F763DF /* Security.framework in Frameworks */,
290					15D2CFAD18F202D000B6D9F1 /* QuartzCore.framework in Frameworks */,
291					1FE4FE59148E4CDD008EDE8B /* Cocoa.framework in Frameworks */,
292					15A89D2B25F2C5F1003D33F5 /* PXSourceList.framework in Frameworks */,
293				);
294				runOnlyForDeploymentPostprocessing = 0;
295			};
296			D261C9BD1B852FA300409803 /* Frameworks */ = {
```

> TOOL

tool_use Read
id: toolu_01Rk6gS2mggrB9GBMFq4X76a
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcodeproj/project.pbxproj",
  "offset": 448,
  "limit": 12
}
```

> TOOL

tool_result
id: toolu_01Rk6gS2mggrB9GBMFq4X76a
```
448				name = Products;
449				sourceTree = "<group>";
450			};
451			1FE4FE57148E4CDD008EDE8B /* Frameworks */ = {
452				isa = PBXGroup;
453				children = (
454					15A89D2A25F2C5F1003D33F5 /* PXSourceList.framework */,
455					D2CC8CA61B90F04C00F763DF /* Security.framework */,
456					15D2CFAC18F202D000B6D9F1 /* QuartzCore.framework */,
457					1FE4FE58148E4CDD008EDE8B /* Cocoa.framework */,
458					1FE4FE5A148E4CDD008EDE8B /* Other Frameworks */,
459				);
```

> TOOL

tool_use Read
id: toolu_01UiUJyrCdVH1TsUuQnjJAid
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcodeproj/project.pbxproj",
  "offset": 1044,
  "limit": 6
}
```

> TOOL

tool_result
id: toolu_01UiUJyrCdVH1TsUuQnjJAid
```
1044					MACOSX_DEPLOYMENT_TARGET = 26.0;
1045					ONLY_ACTIVE_ARCH = NO;
1046					PRODUCT_BUNDLE_IDENTIFIER = "com.scottdensmore.--PRODUCT-NAME-rfc1034identifier-";
1047					"PRODUCT_BUNDLE_IDENTIFIER[sdk=macosx*]" = com.scottdensmore.Cakebrew;
1048					PRODUCT_NAME = Cakebrew;
1049					PROVISIONING_PROFILE_SPECIFIER = "";
```

> TOOL

tool_use Read
id: toolu_01Xc1GoPyVxdvPk9ychmgE4C
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcodeproj/project.pbxproj",
  "offset": 1049,
  "limit": 4
}
```

> TOOL

tool_result
id: toolu_01Xc1GoPyVxdvPk9ychmgE4C
```
1049					PROVISIONING_PROFILE_SPECIFIER = "";
1050					USER_HEADER_SEARCH_PATHS = "$(PROJECT_DIR)/Cakebrew/Frameworks/PXSourceList.framework/Headers";
1051					WRAPPER_EXTENSION = app;
1052				};
```

> TOOL

tool_use Read
id: toolu_01R7HsgLrCLr77h4PHmAEZCj
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcodeproj/project.pbxproj",
  "offset": 1085,
  "limit": 4
}
```

> TOOL

tool_result
id: toolu_01R7HsgLrCLr77h4PHmAEZCj
```
1085					PRODUCT_NAME = Cakebrew;
1086					PROVISIONING_PROFILE_SPECIFIER = "";
1087					USER_HEADER_SEARCH_PATHS = "$(PROJECT_DIR)/Cakebrew/Frameworks/PXSourceList.framework/Headers";
1088					WRAPPER_EXTENSION = app;
```

> AGENT

I have everything I need. The build breaks because the workspace and project still reference the deleted PXSourceList framework/submodule, and the code/XIB still use its classes. I'll migrate to a native `NSOutlineView`. Starting with the implementation.

> TOOL

tool_use mcp__ccd_session__mark_chapter
id: toolu_01DevV7jdF74cHxuv7y5TECR
```json
{
  "title": "Native NSOutlineView migration",
  "summary": "Replace PXSourceList with a native NSOutlineView source list across code, XIB, project, and workspace"
}
```

> TOOL

tool_result
id: toolu_01DevV7jdF74cHxuv7y5TECR
```
Chapter marked: "Native NSOutlineView migration". Continue your current work.
```

> AGENT

Now I'll rewrite the sidebar controller header to drop PXSourceList and define lightweight native replacements.

> TOOL

tool_use Write
id: toolu_01JS3L3E775Vnq5ytFRfH3fh
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/Controllers/BPSideBarController.h",
  "content": "//\n//  BPSideBarController.h\n//  Cakebrew\n//\n//  Created by Marek Hrusovsky on 05/09/14.\n//  Copyright (c) 2014 Bruno Philipe. All rights reserved.\n//\n\n@import Cocoa;\n\ntypedef NS_ENUM(NSUInteger, FormulaeSideBarItem)\n{\n\tFormulaeSideBarItemFormulaeCategory = 0,\n\tFormulaeSideBarItemInstalled = 1,\n\tFormulaeSideBarItemOutdated = 2,\n\tFormulaeSideBarItemAll = 3,\n\tFormulaeSideBarItemLeaves = 4,\n\tFormulaeSideBarItemRepositories = 5,\n\tFormulaeSideBarItemToolsCategory = 6,\n\tFormulaeSideBarItemDoctor = 7,\n\tFormulaeSideBarItemUpdate = 8,\n};\n\n@protocol BPSideBarControllerDelegate <NSObject>\n- (void)sourceListSelectionDidChange;\n@end\n\n@interface BPSidebarItem : NSObject\n\n@property (copy) NSString *title;\n@property (copy) NSString *identifier;\n@property (strong) NSImage *icon;\n@property (strong) NSNumber *badgeValue;\n@property (readonly) NSArray<BPSidebarItem *> *children;\n\n+ (instancetype)itemWithTitle:(NSString *)title identifier:(NSString *)identifier;\n- (void)addChildItem:(BPSidebarItem *)item;\n- (BOOL)hasChildren;\n\n@end\n\n@interface BPSidebarBadgeView : NSView\n\n@property (nonatomic) NSUInteger badgeValue;\n@property (nonatomic, getter=isEmphasized) BOOL emphasized;\n\n@end\n\n@interface BPSidebarTableCellView : NSTableCellView\n\n@property (assign) IBOutlet BPSidebarBadgeView *badgeView;\n\n@end\n\n@interface BPSideBarController : NSObject <NSOutlineViewDataSource, NSOutlineViewDelegate>\n\n@property (assign) IBOutlet NSOutlineView *sidebar;\n\n@property (weak) id <BPSideBarControllerDelegate>delegate;\n\n- (void)refreshSidebarBadges;\n- (void)configureSidebarSettings;\n\n- (IBAction)selectSideBarRowWithSenderTag:(id)sender;\n\n@end\n"
}
```

> TOOL

tool_result
id: toolu_01JS3L3E775Vnq5ytFRfH3fh
```
The file /home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/Controllers/BPSideBarController.h has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now the implementation file — rewriting the data source/delegate for `NSOutlineView` and adding the model, cell, and badge view implementations.

> TOOL

tool_use Write
id: toolu_01MKytH91bgWZuru8XjTKCre
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/Controllers/BPSideBarController.m",
  "content": "//\n//  BPSideBarController.m\n//  Cakebrew\n//\n//  Created by Marek Hrusovsky on 05/09/14.\n//  Copyright (c) 2014 Bruno Philipe. All rights reserved.\n//\n\n#import \"BPSideBarController.h\"\n#import \"BPHomebrewManager.h\"\n\n@interface BPSidebarItem ()\n@property (strong) NSMutableArray<BPSidebarItem *> *mutableChildren;\n@end\n\n@implementation BPSidebarItem\n\n+ (instancetype)itemWithTitle:(NSString *)title identifier:(NSString *)identifier\n{\n\tBPSidebarItem *item = [[self alloc] init];\n\titem.title = title;\n\titem.identifier = identifier;\n\treturn item;\n}\n\n- (instancetype)init\n{\n\tself = [super init];\n\tif (self) {\n\t\t_mutableChildren = [NSMutableArray array];\n\t}\n\treturn self;\n}\n\n- (NSArray<BPSidebarItem *> *)children\n{\n\treturn self.mutableChildren;\n}\n\n- (void)addChildItem:(BPSidebarItem *)item\n{\n\t[self.mutableChildren addObject:item];\n}\n\n- (BOOL)hasChildren\n{\n\treturn self.mutableChildren.count > 0;\n}\n\n@end\n\n#pragma mark -\n\n@implementation BPSidebarBadgeView\n\n- (void)setBadgeValue:(NSUInteger)badgeValue\n{\n\tif (_badgeValue != badgeValue) {\n\t\t_badgeValue = badgeValue;\n\t\t[self invalidateIntrinsicContentSize];\n\t\t[self setNeedsDisplay:YES];\n\t}\n}\n\n- (void)setEmphasized:(BOOL)emphasized\n{\n\tif (_emphasized != emphasized) {\n\t\t_emphasized = emphasized;\n\t\t[self setNeedsDisplay:YES];\n\t}\n}\n\n- (NSString *)badgeText\n{\n\treturn [NSString stringWithFormat:@\"%lu\", (unsigned long)self.badgeValue];\n}\n\n- (NSDictionary *)textAttributesWithColor:(NSColor *)color\n{\n\treturn @{ NSFontAttributeName: [NSFont boldSystemFontOfSize:11.0],\n\t\t\t  NSForegroundColorAttributeName: color };\n}\n\n- (NSSize)intrinsicContentSize\n{\n\tNSSize textSize = [[self badgeText] sizeWithAttributes:[self textAttributesWithColor:NSColor.labelColor]];\n\treturn NSMakeSize(ceil(textSize.width) + 14.0, 16.0);\n}\n\n- (void)drawRect:(NSRect)dirtyRect\n{\n\tNSColor *backgroundColor;\n\tNSColor *textColor;\n\tif (self.isEmphasized) {\n\t\tbackgroundColor = [NSColor.whiteColor colorWithAlphaComponent:0.9];\n\t\ttextColor = NSColor.selectedContentBackgroundColor;\n\t} else {\n\t\tbackgroundColor = [NSColor.secondaryLabelColor colorWithAlphaComponent:0.18];\n\t\ttextColor = NSColor.secondaryLabelColor;\n\t}\n\n\tCGFloat pillHeight = 16.0;\n\tNSRect pill = NSMakeRect(NSMinX(self.bounds),\n\t\t\t\t\t\t\t NSMidY(self.bounds) - pillHeight / 2.0,\n\t\t\t\t\t\t\t NSWidth(self.bounds),\n\t\t\t\t\t\t\t pillHeight);\n\tNSBezierPath *path = [NSBezierPath bezierPathWithRoundedRect:pill\n\t\t\t\t\t\t\t\t\t\t\t\t\t\txRadius:pillHeight / 2.0\n\t\t\t\t\t\t\t\t\t\t\t\t\t\tyRadius:pillHeight / 2.0];\n\t[backgroundColor setFill];\n\t[path fill];\n\n\tNSString *text = [self badgeText];\n\tNSDictionary *attributes = [self textAttributesWithColor:textColor];\n\tNSSize textSize = [text sizeWithAttributes:attributes];\n\tNSPoint origin = NSMakePoint(NSMidX(pill) - textSize.width / 2.0,\n\t\t\t\t\t\t\t\t NSMidY(pill) - textSize.height / 2.0);\n\t[text drawAtPoint:origin withAttributes:attributes];\n}\n\n@end\n\n#pragma mark -\n\n@implementation BPSidebarTableCellView\n\n- (void)setBackgroundStyle:(NSBackgroundStyle)backgroundStyle\n{\n\t[super setBackgroundStyle:backgroundStyle];\n\tself.badgeView.emphasized = (backgroundStyle == NSBackgroundStyleEmphasized);\n}\n\n@end\n\n#pragma mark -\n\n@interface BPSideBarController()\n\n@property (strong, nonatomic) BPSidebarItem *rootSidebarCategory;\n\n@property (strong, […]

> TOOL

tool_result
id: toolu_01MKytH91bgWZuru8XjTKCre
```
The file /home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/Controllers/BPSideBarController.m has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now remove the PXSourceList import from the view controller header.

> TOOL

tool_use Edit
id: toolu_01MKsXHmbhpCeHVjmdWrVGKF
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/Controllers/BPHomebrewViewController.h",
  "old_string": "#import <Foundation/Foundation.h>\n#import <PXSourceList/PXSourceList.h>\n#import \"BPFormula.h\"",
  "new_string": "#import <Foundation/Foundation.h>\n#import \"BPFormula.h\""
}
```

> TOOL

tool_result
id: toolu_01MKsXHmbhpCeHVjmdWrVGKF
```
The file /home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/Controllers/BPHomebrewViewController.h has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now the XIB — swap the four custom classes from PXSourceList types to native/our classes.

> TOOL

tool_use Edit
id: toolu_01PfcJ1vkWgfST6UF6E2Uf8L
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/Base.lproj/MainMenu.xib",
  "old_string": "indentationPerLevel=\"13\" outlineTableColumn=\"Dme-LE-cyv\" id=\"9f4-xo-e1c\" customClass=\"PXSourceList\">",
  "new_string": "indentationPerLevel=\"13\" outlineTableColumn=\"Dme-LE-cyv\" id=\"9f4-xo-e1c\">"
}
```

> TOOL

tool_result
id: toolu_01PfcJ1vkWgfST6UF6E2Uf8L
```
The file /home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/Base.lproj/MainMenu.xib has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01JNahwBwVHFBJVCV1W26KuU
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/Base.lproj/MainMenu.xib",
  "old_string": "<tableCellView identifier=\"HeaderCell\" id=\"266-1g-zfm\" customClass=\"PXSourceListTableCellView\">",
  "new_string": "<tableCellView identifier=\"HeaderCell\" id=\"266-1g-zfm\" customClass=\"BPSidebarTableCellView\">"
}
```

> TOOL

tool_result
id: toolu_01JNahwBwVHFBJVCV1W26KuU
```
The file /home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/Base.lproj/MainMenu.xib has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01SR2WdsGHPxcuc7UfMa1cA5
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/Base.lproj/MainMenu.xib",
  "old_string": "<tableCellView identifier=\"MainCell\" id=\"Emw-wX-GZR\" customClass=\"PXSourceListTableCellView\">",
  "new_string": "<tableCellView identifier=\"MainCell\" id=\"Emw-wX-GZR\" customClass=\"BPSidebarTableCellView\">"
}
```

> TOOL

tool_result
id: toolu_01SR2WdsGHPxcuc7UfMa1cA5
```
The file /home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/Base.lproj/MainMenu.xib has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_011Pc1PDDqfRHAbEsopgbdD5
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/Base.lproj/MainMenu.xib",
  "old_string": "placeholderIntrinsicWidth=\"40\" placeholderIntrinsicHeight=\"16\" translatesAutoresizingMaskIntoConstraints=\"NO\" id=\"NXZ-4S-anG\" customClass=\"PXSourceListBadgeView\">",
  "new_string": "placeholderIntrinsicWidth=\"40\" placeholderIntrinsicHeight=\"16\" translatesAutoresizingMaskIntoConstraints=\"NO\" id=\"NXZ-4S-anG\" customClass=\"BPSidebarBadgeView\">"
}
```

> TOOL

tool_result
id: toolu_011Pc1PDDqfRHAbEsopgbdD5
```
The file /home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/Base.lproj/MainMenu.xib has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now remove the dead PXSourceList project reference from the workspace.

> TOOL

tool_use Edit
id: toolu_01PEiyuLi7qT1XyRj5vN4R3Z
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcworkspace/contents.xcworkspacedata",
  "old_string": "   <FileRef\n      location = \"container:Cakebrew.xcodeproj\">\n   </FileRef>\n   <FileRef\n      location = \"group:Dependencies/PXSourceList/PXSourceList.xcodeproj\">\n   </FileRef>\n</Workspace>",
  "new_string": "   <FileRef\n      location = \"container:Cakebrew.xcodeproj\">\n   </FileRef>\n</Workspace>"
}
```

> TOOL

tool_result
id: toolu_01PEiyuLi7qT1XyRj5vN4R3Z
```
The file /home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcworkspace/contents.xcworkspacedata has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now remove the 8 PXSourceList references from the project file.

> TOOL

tool_use Edit
id: toolu_01SRcDYWsviiVPzHeAjPhiHn
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcodeproj/project.pbxproj",
  "old_string": "\t\t15A89D2B25F2C5F1003D33F5 /* PXSourceList.framework in Frameworks */ = {isa = PBXBuildFile; fileRef = 15A89D2A25F2C5F1003D33F5 /* PXSourceList.framework */; };\n\t\t15A89D2C25F2C5F1003D33F5 /* PXSourceList.framework in CopyFiles */ = {isa = PBXBuildFile; fileRef = 15A89D2A25F2C5F1003D33F5 /* PXSourceList.framework */; settings = {ATTRIBUTES = (CodeSignOnCopy, RemoveHeadersOnCopy, ); }; };\n\t\t15A89D3925F2F467003D33F5 /* NSLayoutConstraint+Shims.m in Sources */",
  "new_string": "\t\t15A89D3925F2F467003D33F5 /* NSLayoutConstraint+Shims.m in Sources */"
}
```

> TOOL

tool_result
id: toolu_01SRcDYWsviiVPzHeAjPhiHn
```
The file /home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcodeproj/project.pbxproj has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_0152rXcE3aLAfvEatBR4VrLD
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcodeproj/project.pbxproj",
  "old_string": "\t\t\tfiles = (\n\t\t\t\t15A89D2C25F2C5F1003D33F5 /* PXSourceList.framework in CopyFiles */,\n\t\t\t);\n\t\t\trunOnlyForDeploymentPostprocessing = 0;\n\t\t};\n/* End PBXCopyFilesBuildPhase section */",
  "new_string": "\t\t\tfiles = (\n\t\t\t);\n\t\t\trunOnlyForDeploymentPostprocessing = 0;\n\t\t};\n/* End PBXCopyFilesBuildPhase section */"
}
```

> TOOL

tool_result
id: toolu_0152rXcE3aLAfvEatBR4VrLD
```
The file /home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcodeproj/project.pbxproj has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_012YUdzJ1S28NYwaZRWtmnoY
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcodeproj/project.pbxproj",
  "old_string": "\t\t15A89D2A25F2C5F1003D33F5 /* PXSourceList.framework */ = {isa = PBXFileReference; explicitFileType = wrapper.framework; path = PXSourceList.framework; sourceTree = BUILT_PRODUCTS_DIR; };\n",
  "new_string": ""
}
```

> TOOL

tool_result
id: toolu_012YUdzJ1S28NYwaZRWtmnoY
```
The file /home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcodeproj/project.pbxproj has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01Rnw6c7gwTZrABK4FTUNciz
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcodeproj/project.pbxproj",
  "old_string": "\t\t\t\t1FE4FE59148E4CDD008EDE8B /* Cocoa.framework in Frameworks */,\n\t\t\t\t15A89D2B25F2C5F1003D33F5 /* PXSourceList.framework in Frameworks */,\n\t\t\t);",
  "new_string": "\t\t\t\t1FE4FE59148E4CDD008EDE8B /* Cocoa.framework in Frameworks */,\n\t\t\t);"
}
```

> TOOL

tool_result
id: toolu_01Rnw6c7gwTZrABK4FTUNciz
```
The file /home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcodeproj/project.pbxproj has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01EJsMNUA47VjqFZeSjk4pVv
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcodeproj/project.pbxproj",
  "old_string": "\t\t\tchildren = (\n\t\t\t\t15A89D2A25F2C5F1003D33F5 /* PXSourceList.framework */,\n\t\t\t\tD2CC8CA61B90F04C00F763DF /* Security.framework */,",
  "new_string": "\t\t\tchildren = (\n\t\t\t\tD2CC8CA61B90F04C00F763DF /* Security.framework */,"
}
```

> TOOL

tool_result
id: toolu_01EJsMNUA47VjqFZeSjk4pVv
```
The file /home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcodeproj/project.pbxproj has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_016EjXv7U5cQM1XvZg3g59M4
```json
{
  "replace_all": true,
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcodeproj/project.pbxproj",
  "old_string": "\t\t\t\tPROVISIONING_PROFILE_SPECIFIER = \"\";\n\t\t\t\tUSER_HEADER_SEARCH_PATHS = \"$(PROJECT_DIR)/Cakebrew/Frameworks/PXSourceList.framework/Headers\";\n\t\t\t\tWRAPPER_EXTENSION = app;",
  "new_string": "\t\t\t\tPROVISIONING_PROFILE_SPECIFIER = \"\";\n\t\t\t\tWRAPPER_EXTENSION = app;"
}
```

> TOOL

tool_result
id: toolu_016EjXv7U5cQM1XvZg3g59M4
```
The file /home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcodeproj/project.pbxproj has been updated. All occurrences were successfully replaced. (file state is current in your context — no need to Read it back)
```

> AGENT

All edits are done. Let me verify no PXSourceList references remain, then build.

> TOOL

tool_use Bash
id: toolu_01AvRGTEn4rnYarFvhPdc7vY
```json
{
  "command": "grep -rn \"PXSourceList\" Cakebrew Cakebrew.xcodeproj/project.pbxproj Cakebrew.xcworkspace 2>/dev/null; echo \"EXIT: $?\"",
  "description": "Confirm no PXSourceList references remain"
}
```

> TOOL

tool_use Bash
id: toolu_01Et68d78t8iPFzddScRJBXL
```json
{
  "command": "xcodebuild -list -workspace Cakebrew.xcworkspace 2>&1 | head -30",
  "description": "List workspace schemes to confirm workspace is valid"
}
```

> TOOL

tool_result
id: toolu_01AvRGTEn4rnYarFvhPdc7vY
```
Cakebrew/Credits.rtf:57:\ls2\ilvl0\cf0 {\listtext	\uc0\u8226 	}{\field{\*\fldinst{HYPERLINK "https://github.com/brunophilipe/PXSourceList"}}{\fldrslt PXSourceList}} by Alex Rozanski\
Cakebrew/pt.lproj/Credits.rtf:26:\ls1\ilvl0\cf0 {\listtext	\'95	}{\field{\*\fldinst{HYPERLINK "https://github.com/Perspx/PXSourceList"}}{\fldrslt PXSourceList}} by Alex Rozanski\uc0\u8232 	Copyright \'a9 2009-14, Alex Rozanski and other contributors. All rights reserved.\
EXIT: 0
```

> TOOL

tool_result
id: toolu_01Et68d78t8iPFzddScRJBXL
```
Command line invocation:
    /Applications/Xcode.app/Contents/Developer/usr/bin/xcodebuild -list -workspace Cakebrew.xcworkspace

2026-05-25 15:52:10.032 xcodebuild[15000:161526]  DVTDeviceOperation: Encountered a build number "" that is incompatible with DVTBuildVersion.
2026-05-25 15:52:10.166 xcodebuild[15000:161455] [MT] DVTDeviceOperation: Encountered a build number "" that is incompatible with DVTBuildVersion.
Information about workspace "Cakebrew":
    Schemes:
        Cakebrew
        CakebrewTests
```

> AGENT

Good — the only remaining references are in `Credits.rtf` (attribution text for the original library), which don't affect the build. The workspace now resolves cleanly. Let me build it.

> TOOL

tool_use Bash
id: toolu_01XXXpFoi1mVRQeUgWB5QCgE
```json
{
  "command": "xcodebuild -workspace Cakebrew.xcworkspace -scheme Cakebrew -configuration Debug -destination 'platform=macOS' build 2>&1 | tail -60",
  "description": "Build the Cakebrew app from the workspace",
  "timeout": 420000
}
```

> TOOL

tool_result
id: toolu_01XXXpFoi1mVRQeUgWB5QCgE
```
    cd /home/<USER>/Developer/scottdensmore/cakebrew
    /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/clang -Xlinker -reproducible -target x86_64-apple-macos26.0 -isysroot /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX26.5.sdk -O0 -L/home/<USER>/Library/Developer/Xcode/DerivedData/Cakebrew-ejkvoljwklzjefduqadkgzlgzyoq/Build/Intermediates.noindex/EagerLinkingTBDs/Debug -L/home/<USER>/Library/Developer/Xcode/DerivedData/Cakebrew-ejkvoljwklzjefduqadkgzlgzyoq/Build/Products/Debug -F/home/<USER>/Library/Developer/Xcode/DerivedData/Cakebrew-ejkvoljwklzjefduqadkgzlgzyoq/Build/Intermediates.noindex/EagerLinkingTBDs/Debug -F/home/<USER>/Library/Developer/Xcode/DerivedData/Cakebrew-ejkvoljwklzjefduqadkgzlgzyoq/Build/Products/Debug -F/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/Frameworks -filelist /home/<USER>/Library/Developer/Xcode/DerivedData/Cakebrew-ejkvoljwklzjefduqadkgzlgzyoq/Build/Intermediates.noindex/Cakebrew.build/Debug/Cakebrew.build/Objects-normal/x86_64/Cakebrew.LinkFileList -Xlinker -rpath -Xlinker @executable_path/../Frameworks -Xlinker -dead_strip -Xlinker -object_path_lto -Xlinker /home/<USER>/Library/Developer/Xcode/DerivedData/Cakebrew-ejkvoljwklzjefduqadkgzlgzyoq/Build/Intermediates.noindex/Cakebrew.build/Debug/Cakebrew.build/Objects-normal/x86_64/Cakebrew_lto.o -rdynamic -Xlinker -no_deduplicate -Xlinker -dependency_info -Xlinker /home/<USER>/Library/Developer/Xcode/DerivedData/Cakebrew-ejkvoljwklzjefduqadkgzlgzyoq/Build/Intermediates.noindex/Cakebrew.build/Debug/Cakebrew.build/Objects-normal/x86_64/Cakebrew_dependency_info.dat -fobjc-arc -fobjc-link-runtime -framework Security -framework QuartzCore -framework Cocoa -Xlinker -no_adhoc_codesign -o /home/<USER>/Library/Developer/Xcode/DerivedData/Cakebrew-ejkvoljwklzjefduqadkgzlgzyoq/Build/Intermediates.noindex/Cakebrew.build/Debug/Cakebrew.build/Objects-normal/x86_64/Binary/Cakebrew

PrecompileModule /home/<USER>/Library/Developer/Xcode/DerivedData/Cakebrew-ejkvoljwklzjefduqadkgzlgzyoq/Build/Intermediates.noindex/ExplicitPrecompiledModules/REDACTED.scan
    cd /
    builtin-precompileModule /home/<USER>/Library/Developer/Xcode/DerivedData/Cakebrew-ejkvoljwklzjefduqadkgzlgzyoq/Build/Intermediates.noindex/ExplicitPrecompiledModules/REDACTED.scan

CompileC /home/<USER>/Library/Developer/Xcode/DerivedData/Cakebrew-ejkvoljwklzjefduqadkgzlgzyoq/Build/Intermediates.noindex/Cakebrew.build/Debug/Cakebrew.build/Objects-normal/arm64/BPAppDelegate.o /home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/BPAppDelegate.m normal arm64 objective-c com.apple.compilers.llvm.clang.1_0.compiler (in target 'Cakebrew' from project 'Cakebrew')
    cd /home/<USER>/Developer/scottdensmore/cakebrew
    
    Using response file: /home/<USER>/Library/Developer/Xcode/DerivedData/Cakebrew-ejkvoljwklzjefduqadkgzlgzyoq/Build/Intermediates.noindex/Cakebrew.build/Debug/Cakebrew.build/Objects-normal/arm64/e6072d4f65d7061329687fe24e3d63a7-common-args.resp
    
    /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/clang -x objective-c -ivfsstatcache /home/<USER>/Library/Developer/Xcode/DerivedData/SDKStatCaches.noindex/macosx26.5-25F70-e082c4a02f00227109f4ed75e425c832.sdkstatcache -target arm64-apple-macos26.0 -fmessage-length\=0 -fdiagnostics-show-note-include-stack -fmacro-backtrace-limit\=0 -fno-color-diagnostics -fmodules-prune-interval\=86400 -fmodules-prune-after\=345600 -fbuild-session-file\=/home/<USER>/Library/Developer/Xcode/DerivedData/ModuleCache.noindex/Session.modulevalidation -fmodules-validate-once-per-build-session -Wnon-modular-include-in-framework-module -Werror\=non-modular-include-in-framework-module -Wno-trigraphs -Wno-missing-field-initializers -Wmissing-prototypes -Wunreachable-code -Wquoted-include-in-framework-header -Wno-implicit-atomic-properties -Wno-objc-interface-ivars -Wno-arc-repeated-use-of-weak -Wexplicit-ownership-type -Wimplicit-retain-self -Wduplicate-method-match -Wno-missing-braces -Wparentheses -Wswitch -Wunused-function -Wno-unused-label -Wno-unused-parameter -Wunused-variable -Wunused-value -Wempty-body -Wuninitialized -Wno-unknown-pragmas -Wno-shadow -Wno-four-char-constants -Wno-conversion -Wconstant-conversion -Wint-conversion -Wbool-conversion -Wenum-conversion -Wno-float-conversion -Wnon-literal-null-conversion -Wobjc-literal-conversion -Wshorten-64-to-32 -Wpointer-sign -Wno-newline-eof -Wno-selector -Wno-strict-selector-match -Wundeclared-selector -Wdeprecated-implementations -Wno-implicit-fallthrough -isysroot /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX26.5.sdk -fstrict-aliasing -Wprotocol -Wdeprecated-declarations -Wno-sign-conversion -Winfinite-recursion -Wcomma -Wblock-capture-autoreleasing -Wstrict-prototypes -Wno-semicolon-before-method-body -index-store-path /home/<USER>/Library/Developer/Xcode/DerivedData/Cakebrew-ejkvoljwklzjefduqadkgzlgzyoq/Index.noindex/DataStore @/home/<USER>/Library/Developer/Xcode/DerivedData/Cakebrew-ejkvoljwklzjefduqadkgzlgzyoq/Build/Intermediates.noindex/Cakebrew.build/Debug/Cakebrew.build/Objects-normal/arm64/e6072d4f65d7061329687fe24e3d63a7-common-args.resp -include /home/<USER>/Library/Developer/Xcode/DerivedData/Cakebrew-ejkvoljwklzjefduqadkgzlgzyoq/Build/Intermediates.noindex/PrecompiledHeaders/SharedPrecompiledHeaders/12682132033696376527/Cakebrew-Prefix.pch -MMD -MT dependencies -MF /home/<USER>/Library/Developer/Xcode/DerivedData/Cakebrew-ejkvoljwklzjefduqadkgzlgzyoq/Build/Intermediates.noindex/Cakebrew.build/Debug/Cakebrew.build/Objects-normal/arm64/BPAppDelegate.d --serialize-diagnostics /home/<USER>/Library/Developer/Xcode/DerivedData/Cakebrew-ejkvoljwklzjefduqadkgzlgzyoq/Build/Intermediates.noindex/Cakebrew.build/Debug/Cakebrew.build/Objects-normal/arm64/BPAppDelegate.dia -c /home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/BPAppDelegate.m -o /home/<USER>/Library/Developer/Xcode/DerivedData/Cakebrew-ejkvoljwklzjefduqadkgzlgzyoq/Build/Intermediates.noindex/Cakebrew.build/Debug/Cakebrew.build/Objects-normal/arm64/BPAppDelegate.o -index-unit-output-path /Cakebrew.build/Debug/Cakebrew.build/Objects-normal/arm64/BPAppDelegate.o

Ld /home/<USER>/Library/Developer/Xcode/DerivedData/Cakebrew-ejkvoljwklzjefduqadkgzlgzyoq/Build/Products/Debug/CakebrewTests.xctest/Contents/MacOS/CakebrewTests normal (in target 'CakebrewTests' from project 'Cakebrew')
    cd /home/<USER>/Developer/scottdensmore/cakebrew
    /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/clang -Xlinker -reproducible -target x86_64-apple-macos26.0 -bundle -isysroot /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX26.5.sdk -O0 -L/home/<USER>/Library/Developer/Xcode/DerivedData/Cakebrew-ejkvoljwklzjefduqadkgzlgzyoq/Build/Intermediates.noindex/EagerLinkingTBDs/Debug -L/home/<USER>/Library/Developer/Xcode/DerivedData/Cakebrew-ejkvoljwklzjefduqadkgzlgzyoq/Build/Products/Debug -L/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/usr/lib -F/home/<USER>/Library/Developer/Xcode/DerivedData/Cakebrew-ejkvoljwklzjefduqadkgzlgzyoq/Build/Intermediates.noindex/EagerLinkingTBDs/Debug -F/home/<USER>/Library/Developer/Xcode/DerivedData/Cakebrew-ejkvoljwklzjefduqadkgzlgzyoq/Build/Products/Debug -F/Applications/Xcode.app/Contents/Developer/Library/Frameworks -iframework /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/Library/Frameworks -filelist /home/<USER>/Library/Developer/Xcode/DerivedData/Cakebrew-ejkvoljwklzjefduqadkgzlgzyoq/Build/Intermediates.noindex/Cakebrew.build/Debug/CakebrewTests.build/Objects-normal/x86_64/CakebrewTests.LinkFileList -Xlinker -rpath -Xlinker @loader_path/../Frameworks -Xlinker -rpath -Xlinker @executable_path/../Frameworks -Xlinker […]

> AGENT

Build succeeded. Both `Cakebrew.app` and `CakebrewTests` compiled, linked, and signed cleanly with no PXSourceList framework. Let me launch the app to confirm the sidebar renders and it doesn't crash on startup.

> TOOL

tool_use Bash
id: toolu_01D5G7UyyXrNkwbBTBV8yLSk
```json
{
  "command": "APP=\"/home/<USER>/Library/Developer/Xcode/DerivedData/Cakebrew-ejkvoljwklzjefduqadkgzlgzyoq/Build/Products/Debug/Cakebrew.app\"; open \"$APP\"; sleep 4; if pgrep -x Cakebrew >/dev/null; then echo \"RUNNING: Cakebrew is alive (pid $(pgrep -x Cakebrew))\"; else echo \"NOT RUNNING — possible crash\"; fi",
  "description": "Launch the built app and check it stays running"
}
```

> TOOL

tool_result
id: toolu_01D5G7UyyXrNkwbBTBV8yLSk
```
RUNNING: Cakebrew is alive (pid 15380)
```

> AGENT

The app is running without crashing — the sidebar is constructed and rendered at launch, so the new data source/delegate path is exercised. Let me capture just the Cakebrew window to visually verify the sidebar.

> TOOL

tool_use Bash
id: toolu_01Coc5sLXtixKYsVi3qXV1CF
```json
{
  "command": "BOUNDS=$(osascript -e 'tell application \"System Events\" to tell (first process whose name is \"Cakebrew\") to get {position, size} of front window' 2>/dev/null); echo \"bounds: $BOUNDS\"; if [ -n \"$BOUNDS\" ]; then X=$(echo $BOUNDS | cut -d, -f1 | tr -d ' '); Y=$(echo $BOUNDS | cut -d, -f2 | tr -d ' '); W=$(echo $BOUNDS | cut -d, -f3 | tr -d ' '); H=$(echo $BOUNDS | cut -d, -f4 | tr -d ' '); OUT=\"/tmp/cakebrew_sidebar.png\"; screencapture -x -R${X},${Y},${W},${H} \"$OUT\" && echo \"saved: $OUT\"; fi",
  "description": "Capture the Cakebrew window region to a temp file"
}
```

> TOOL

tool_result
id: toolu_01Coc5sLXtixKYsVi3qXV1CF
```
bounds:
```

> AGENT

AppleScript returned nothing (likely an Accessibility-permission gate). Let me get the window ID via CoreGraphics and capture just that window.

> TOOL

tool_use Bash
id: toolu_0152hMMU3QfJhzRADjzdy7J8
```json
{
  "command": "WID=$(/usr/bin/python3 -c \"\nimport Quartz\nwins = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionOnScreenOnly | Quartz.kCGWindowListExcludeDesktopElements, Quartz.kCGNullWindowID)\nfor w in wins:\n    if w.get('kCGWindowOwnerName') == 'Cakebrew' and w.get('kCGWindowLayer') == 0:\n        print(int(w['kCGWindowNumber'])); break\n\" 2>/dev/null); echo \"window id: $WID\"; if [ -n \"$WID\" ]; then screencapture -x -o -l\"$WID\" /tmp/cakebrew_sidebar.png && echo \"saved\" && ls -la /tmp/cakebrew_sidebar.png; fi",
  "description": "Find Cakebrew window id via Quartz and capture it"
}
```

> TOOL

tool_result
id: toolu_0152hMMU3QfJhzRADjzdy7J8
```
window id:
```

> TOOL

tool_use Bash
id: toolu_016mLAouUgGNE77fFU7fF7ek
```json
{
  "command": "/usr/bin/python3 -c \"\nimport Quartz\nwins = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionAll, Quartz.kCGNullWindowID)\nfound=False\nfor w in wins:\n    if w.get('kCGWindowOwnerName') == 'Cakebrew':\n        found=True\n        print('id=%s layer=%s name=%r bounds=%s' % (w.get('kCGWindowNumber'), w.get('kCGWindowLayer'), w.get('kCGWindowName'), w.get('kCGWindowBounds')))\nif not found: print('NO Cakebrew windows found')\n\"",
  "description": "List all Cakebrew windows with details"
}
```

> TOOL

tool_result ERROR
id: toolu_016mLAouUgGNE77fFU7fF7ek
```
Exit code 1
Traceback (most recent call last):
  File "<string>", line 2, in <module>
ModuleNotFoundError: No module named 'Quartz'
```

> AGENT

Quartz isn't available for a targeted capture. Rather than full-screen capture, let me check the unified log for any runtime exceptions from the running app (the sidebar's data source, cell building, and custom badge drawing all run during the initial render).

> TOOL

tool_use Bash
id: toolu_01W5rbd4P32LXPaMmGE4g5gE
```json
{
  "command": "log show --last 2m --predicate 'process == \"Cakebrew\"' 2>/dev/null | grep -iE \"exception|unrecognized selector|crash|assert|NSInternalInconsistency|fault|error\" | head -30; echo \"---- exit ----\"; pgrep -x Cakebrew >/dev/null && echo \"still running pid $(pgrep -x Cakebrew)\" || echo \"no longer running\"",
  "description": "Scan unified log for Cakebrew runtime exceptions"
}
```

> TOOL

tool_result
id: toolu_01W5rbd4P32LXPaMmGE4g5gE
```
---- exit ----
still running pid 15380
```

> AGENT

No exceptions logged and the app is still alive — the sidebar rendering path (data source, cell building, badge drawing, group rows) ran clean. Let me grab a full-screen shot with Cakebrew frontmost for visual confirmation.

> TOOL

tool_use Bash
id: toolu_01C2r52AJaaospYCK7fnRiBR
```json
{
  "command": "osascript -e 'tell application \"Cakebrew\" to activate' 2>/dev/null; sleep 1; screencapture -x /tmp/cakebrew_full.png 2>/dev/null && echo \"saved $(ls -la /tmp/cakebrew_full.png | awk '{print $5}') bytes\"",
  "description": "Activate Cakebrew and capture full screen"
}
```

> TOOL

tool_result ERROR
id: toolu_01C2r52AJaaospYCK7fnRiBR
```
Exit code 1
```

> AGENT

Screen capture is blocked (Terminal lacks Screen Recording permission), so I can't grab a visual. I'll be straight about that: I verified the build and a clean, crash-free launch, but I could not visually confirm the sidebar's appearance — the app is running now so you can eyeball it.

Here's where things stand.

## What was broken
Commit `50117e5` removed the `Dependencies/PXSourceList` submodule, but four things still depended on it, so nothing could build:
- The **workspace** ([contents.xcworkspacedata](Cakebrew.xcworkspace/contents.xcworkspacedata)) still referenced the now-missing `PXSourceList.xcodeproj` — this alone breaks the whole workspace.
- The **project** linked, copied, and header-searched `PXSourceList.framework`.
- The **source** (`BPSideBarController`, `BPHomebrewViewController.h`) used PXSourceList classes/protocols.
- The **XIB** set the sidebar and its cells to PXSourceList custom classes.

## What I changed (migrated to native `NSOutlineView`)
- [BPSideBarController.h](Cakebrew/Controllers/BPSideBarController.h) / [.m](Cakebrew/Controllers/BPSideBarController.m) — dropped `@import PXSourceList`; now conform to `NSOutlineViewDataSource/Delegate`. Added small native replacements: `BPSidebarItem` (model), `BPSidebarTableCellView` (cell with a badge outlet), and `BPSidebarBadgeView` (draws the count pill, with selected/normal styling). Group rows use `isGroupItem:` and are kept expanded (`shouldCollapseItem:` → NO) so the existing flat `FormulaeSideBarItem` row indices still line up.
- [BPHomebrewViewController.h](Cakebrew/Controllers/BPHomebrewViewController.h) — removed the PXSourceList import.
- [MainMenu.xib](Cakebrew/Base.lproj/MainMenu.xib) — outline view is now a stock `NSOutlineView` (it already […]

> TOOL

tool_use mcp__ccd_session__spawn_task
id: toolu_01EvBJ5ERSVuEduizBW4CJgw
```json
{
  "title": "Remove PXSourceList from acknowledgements",
  "prompt": "The Cakebrew app removed its PXSourceList dependency (migrated the sidebar to a native NSOutlineView), but the acknowledgements/credits files still list PXSourceList. Remove the PXSourceList attribution entries from Cakebrew/Credits.rtf and Cakebrew/pt.lproj/Credits.rtf (and any other localized Credits.rtf that mentions it). Search for \"PXSourceList\" across the repo's Credits.rtf files. Keep the rest of the credits intact and preserve RTF formatting. Do not touch source code — this is a docs/credits cleanup only.",
  "tldr": "The app no longer uses PXSourceList, but the Credits/acknowledgements still list it. This removes the stale attribution from the Credits.rtf files."
}
```

> TOOL

tool_result
id: toolu_01EvBJ5ERSVuEduizBW4CJgw
```
Noted (position 1). A chip is showing for the user — they can start it in a fresh worktree with one click, or dismiss it. Continue your current work.
```

> AGENT

The app is running so you can take a look at the sidebar. Want me to commit these changes, or would you like to review/adjust the badge styling first?

> DEVELOPER

we should alway create a branch and then create a pr and then sqaush merge

> AGENT

Good to know — I'll save that as a standing preference. Let me also check the current git state so I can apply it correctly.

> TOOL

tool_use Read
id: toolu_01X4up31Yr8NFj13iEwX3WJU
```json
{
  "file_path": "/home/<USER>/.claude/projects/-Users-scottdensmore-Developer-scottdensmore-cakebrew/memory/MEMORY.md"
}
```

> TOOL

tool_result ERROR
id: toolu_01X4up31Yr8NFj13iEwX3WJU
```
File does not exist. Note: your current working directory is /home/<USER>/Developer/scottdensmore/cakebrew.
```

> TOOL

tool_use Bash
id: toolu_01Lb64L8q5c9QiKwkofG5MYC
```json
{
  "command": "git status; echo \"==== branch vs master ====\"; git log --oneline master..HEAD; echo \"==== current branch ====\"; git branch --show-current; echo \"==== remotes ====\"; git remote -v",
  "description": "Check git status, branch, commits ahead of master, remotes"
}
```

> TOOL

tool_result
id: toolu_01Lb64L8q5c9QiKwkofG5MYC
```
On branch modernize-macos26
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   Cakebrew.xcodeproj/project.pbxproj
	modified:   Cakebrew.xcworkspace/contents.xcworkspacedata
	modified:   Cakebrew/Base.lproj/MainMenu.xib
	modified:   Cakebrew/Controllers/BPHomebrewViewController.h
	modified:   Cakebrew/Controllers/BPSideBarController.h
	modified:   Cakebrew/Controllers/BPSideBarController.m

no changes added to commit (use "git add" and/or "git commit -a")
==== branch vs master ====
50117e5 Remove PXSourceList submodule
76c5ffd Remove Sparkle.framework and fix acknowledgements URL handling
==== current branch ====
modernize-macos26
==== remotes ====
origin	https://github.com/scottdensmore/Cakebrew.git (fetch)
origin	https://github.com/scottdensmore/Cakebrew.git (push)
upstream	https://github.com/brunophilipe/Cakebrew.git (fetch)
upstream	https://github.com/brunophilipe/Cakebrew.git (push)
```

> AGENT

I'll save that workflow as a standing preference.

> TOOL

tool_use Write
id: toolu_018CHqpSYESEUUifvmKGdbhc
```json
{
  "file_path": "/home/<USER>/.claude/projects/-Users-scottdensmore-Developer-scottdensmore-cakebrew/memory/feedback_git_workflow.md",
  "content": "---\nname: feedback-git-workflow\ndescription: Preferred git workflow for changes — branch, PR, then squash merge (never commit straight to master)\nmetadata:\n  type: feedback\n---\n\nFor any change, use this workflow: create a branch → open a pull request → squash merge it. Do not commit directly to master.\n\n**Why:** The user stated this as their standard process for this project (Cakebrew). Keeps master history clean (one squashed commit per logical change) and routes everything through PR review.\n\n**How to apply:** When work is ready to land, ensure it's on a feature branch (not master), push it, and open a PR against master. Merge via squash merge. Confirm the PR base/repo before pushing or merging, since those are shared/irreversible actions. Origin remote is `scottdensmore/Cakebrew` (their fork); `upstream` is `brunophilipe/Cakebrew`.\n"
}
```

> TOOL

tool_result
id: toolu_018CHqpSYESEUUifvmKGdbhc
```
File created successfully at: /home/<USER>/.claude/projects/-Users-scottdensmore-Developer-scottdensmore-cakebrew/memory/feedback_git_workflow.md (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Write
id: toolu_01AAUQsTpL7CwG4oPHu63gbN
```json
{
  "file_path": "/home/<USER>/.claude/projects/-Users-scottdensmore-Developer-scottdensmore-cakebrew/memory/MEMORY.md",
  "content": "# Memory Index\n\n## Feedback\n- [Git workflow](feedback_git_workflow.md) — always branch → PR → squash merge; never commit straight to master\n"
}
```

> TOOL

tool_result
id: toolu_01AAUQsTpL7CwG4oPHu63gbN
```
File created successfully at: /home/<USER>/.claude/projects/-Users-scottdensmore-Developer-scottdensmore-cakebrew/memory/MEMORY.md (file state is current in your context — no need to Read it back)
```

> AGENT

Saved. Now for applying it — there's a wrinkle I want to confirm before I push or merge anything (those are shared/irreversible).

You're already on the `modernize-macos26` branch, which is **2 commits ahead of master** (Sparkle removal + PXSourceList submodule removal), plus the uncommitted migration work. So a PR from this branch into master would bundle all three together.

> TOOL

tool_use AskUserQuestion
id: toolu_01HYcQie6Jz9WJHRTCQxo1ja
```json
{
  "questions": [
    {
      "question": "Which branch should this PR come from?",
      "header": "Branch",
      "multiSelect": false,
      "options": [
        {
          "label": "Use modernize-macos26",
          "description": "Commit the migration here and PR the whole branch (Sparkle removal + PXSourceList submodule removal + native NSOutlineView migration) into master. Squash collapses it to one commit."
        },
        {
          "label": "New branch for just this fix",
          "description": "Branch off the current point for only the PXSourceList migration commit, leaving the earlier commits for a separate PR. Note: the migration depends on the submodule-removal commit, so the new branch still starts from modernize-macos26."
        }
      ]
    },
    {
      "question": "How far should I take it?",
      "header": "Merge",
      "multiSelect": false,
      "options": [
        {
          "label": "Open PR, let me review",
          "description": "Commit, push to origin, and open the PR against master. Stop there so you can review before merging."
        },
        {
          "label": "Open PR and squash merge now",
          "description": "Commit, push, open the PR against origin/master, and squash merge it immediately without manual review."
        }
      ]
    }
  ]
}
```

> TOOL

tool_result
id: toolu_01HYcQie6Jz9WJHRTCQxo1ja
```
Your questions have been answered: "Which branch should this PR come from?"="Use modernize-macos26", "How far should I take it?"="Open PR, let me review". You can now continue with these answers in mind.
```

> AGENT

Plan set: commit the migration onto `modernize-macos26`, push, open the PR against master, and stop for your review. Let me check the commit-message style and confirm the diff, then commit.

> TOOL

tool_use Bash
id: toolu_01Vkr6Lu45j8meK1cLcpm3s1
```json
{
  "command": "git log --oneline -6; echo \"==== diffstat of working changes ====\"; git diff --stat; echo \"==== upstream tracking ====\"; git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || echo \"(no upstream set for modernize-macos26)\"",
  "description": "Check commit style, working diff, and branch tracking"
}
```

> TOOL

tool_result
id: toolu_01Vkr6Lu45j8meK1cLcpm3s1
```
50117e5 Remove PXSourceList submodule
76c5ffd Remove Sparkle.framework and fix acknowledgements URL handling
1053fe6 Bump build to 594
56eac5c Revert fix for Sidebar
db35975 Bump build to 593
351cddf Update credits file
==== diffstat of working changes ====
 Cakebrew.xcodeproj/project.pbxproj              |   8 -
 Cakebrew.xcworkspace/contents.xcworkspacedata   |   3 -
 Cakebrew/Base.lproj/MainMenu.xib                |   8 +-
 Cakebrew/Controllers/BPHomebrewViewController.h |   1 -
 Cakebrew/Controllers/BPSideBarController.h      |  34 ++-
 Cakebrew/Controllers/BPSideBarController.m      | 263 ++++++++++++++++++------
 6 files changed, 231 insertions(+), 86 deletions(-)
==== upstream tracking ====
(no upstream set for modernize-macos26)
```

> AGENT

Diff is exactly the six files I changed. Committing now.

> TOOL

tool_use Bash
id: toolu_01HwvW6iSawK1MSeuWFhQqJg
```json
{
  "command": "git add Cakebrew.xcodeproj/project.pbxproj Cakebrew.xcworkspace/contents.xcworkspacedata Cakebrew/Base.lproj/MainMenu.xib Cakebrew/Controllers/BPHomebrewViewController.h Cakebrew/Controllers/BPSideBarController.h Cakebrew/Controllers/BPSideBarController.m && git commit -m \"$(cat <<'EOF'\nMigrate sidebar from PXSourceList to native NSOutlineView\n\nThe PXSourceList submodule was removed but the app still depended on it,\nbreaking the build. Replace it with a native NSOutlineView source list:\nadd lightweight BPSidebarItem/BPSidebarTableCellView/BPSidebarBadgeView\nclasses, reimplement the data source and delegate against NSOutlineView,\nand drop the framework references from the project and workspace.\n\nCo-Authored-By: Claude Opus 4.7 (1M context) <<REDACTED_EMAIL>>\nEOF\n)\" && echo \"==== status ====\" && git status",
  "description": "Stage the six files and commit the migration"
}
```

> TOOL

tool_result
id: toolu_01HwvW6iSawK1MSeuWFhQqJg
```
[modernize-macos26 952d98a] Migrate sidebar from PXSourceList to native NSOutlineView
 6 files changed, 231 insertions(+), 86 deletions(-)
==== status ====
On branch modernize-macos26
nothing to commit, working tree clean
```

> AGENT

Committed. Now push the branch to origin and open the PR against master.

> TOOL

tool_use Bash
id: toolu_01EUpsiAnwXZqwCzqmSLWoft
```json
{
  "command": "git push -u origin modernize-macos26 2>&1 | tail -15",
  "description": "Push branch to origin with upstream tracking"
}
```

> TOOL

tool_result
id: toolu_01EUpsiAnwXZqwCzqmSLWoft
```
To https://github.com/scottdensmore/Cakebrew.git
   50117e5..952d98a  modernize-macos26 -> modernize-macos26
branch 'modernize-macos26' set up to track 'origin/modernize-macos26'.
```

> AGENT

Pushed. Now opening the PR against `master` on your fork.

> TOOL

tool_use Bash
id: toolu_01Lr6ve2Hvr3eQ2csfp9duPc
```json
{
  "command": "gh pr create --repo scottdensmore/Cakebrew --base master --head modernize-macos26 --title \"Modernize for macOS 26: drop Sparkle & PXSourceList\" --body \"$(cat <<'EOF'\n## Summary\n- Removes the **Sparkle.framework** vendored binary and fixes acknowledgements URL handling.\n- Removes the **PXSourceList** git submodule.\n- Migrates the sidebar from PXSourceList to a **native `NSOutlineView`** source list, which restores the build:\n  - Adds lightweight `BPSidebarItem` (model), `BPSidebarTableCellView` (cell), and `BPSidebarBadgeView` (count pill) classes in `BPSideBarController`.\n  - Reimplements the data source/delegate against `NSOutlineView`; group rows stay expanded so the existing `FormulaeSideBarItem` row indices still line up.\n  - Drops all `PXSourceList.framework` references from `project.pbxproj` and the stale `PXSourceList.xcodeproj` ref from the workspace.\n\n## Why\nThe PXSourceList submodule was removed earlier, but the code, Xcode project, and workspace still depended on it, so the app would not build. PXSourceList is just an old `NSOutlineView` wrapper; modern AppKit provides the source-list look natively.\n\n## Test plan\n- [x] `xcodebuild -workspace Cakebrew.xcworkspace -scheme Cakebrew` → BUILD SUCCEEDED (app + tests)\n- [x] App launches and stays running; no exceptions in the unified log\n- [ ] Visual check of the sidebar: group headers (Formulae / Tools), item icons, and count badges (including a selected row's badge)\n- [ ] Confirm sidebar selection still drives […]

> TOOL

tool_result
id: toolu_01Lr6ve2Hvr3eQ2csfp9duPc
```
https://github.com/scottdensmore/Cakebrew/pull/1
```

> AGENT

Done. The migration is committed, pushed, and up for review — I stopped short of merging as you asked.

**PR:** [scottdensmore/Cakebrew#1 — Modernize for macOS 26: drop Sparkle & PXSourceList](https://github.com/scottdensmore/Cakebrew/pull/1)

It bundles all three commits on `modernize-macos26` (Sparkle removal, PXSourceList submodule removal, native `NSOutlineView` migration). When you're happy with it, squash-merge it on GitHub (or tell me and I'll do the squash merge).

Also saved your branch → PR → squash-merge workflow to memory so I follow it by default going forward. The built app is still running if you want to eyeball the sidebar before merging.

> DEVELOPER

Ok check the pr and see if there are any comments and if so resolve them (Copilot reviews the code)

> AGENT

I'll check the PR for review comments from Copilot.

> TOOL

tool_use Bash
id: toolu_017veNHDEtuz2Apgx48YTiKY
```json
{
  "command": "echo \"==== PR reviews ====\"; gh pr view 1 --repo scottdensmore/Cakebrew --json reviews,state,mergeable,reviewDecision; echo \"==== review comments (inline) ====\"; gh api repos/scottdensmore/Cakebrew/pulls/1/comments --jq '.[] | {user: .user.login, path: .path, line: .line, body: .body}'; echo \"==== issue comments ====\"; gh api repos/scottdensmore/Cakebrew/issues/1/comments --jq '.[] | {user: .user.login, body: .body}'",
  "description": "Fetch PR reviews and all comments"
}
```

> TOOL

tool_result
id: toolu_017veNHDEtuz2Apgx48YTiKY
```
==== PR reviews ====
{"mergeable":"MERGEABLE","reviewDecision":"","reviews":[{"id":"PRR_kwDOA4x9PM8AAAABA9QKGQ","author":{"login":"copilot-pull-request-reviewer"},"authorAssociation":"NONE","body":"## Pull request overview\n\nModernizes Cakebrew’s macOS integration by removing legacy vendored dependencies (Sparkle, PXSourceList) and reworking the sidebar to use native AppKit (`NSOutlineView`), along with a few related platform updates.\n\n**Changes:**\n- Remove vendored Sparkle framework files and related workspace/project wiring.\n- Remove PXSourceList dependency and migrate the sidebar UI/data source to native `NSOutlineView` with custom item/cell/badge types.\n- Update app behavior for newer macOS APIs (e.g., UserNotifications, toolbar items, event types) and refresh Xcode project/workspace metadata.\n\n### Reviewed changes\n\nCopilot reviewed 57 out of 215 changed files in this pull request and generated 8 comments.\n\n<details>\n<summary>Show a summary per file</summary>\n\n| File | Description |\r\n| ---- | ----------- |\r\n| CakebrewTests/BPFormulaTests.m | Trailing whitespace/newlines only. |\r\n| Cakebrew/Libraries/DCOAboutWindow/DCOAboutWindowController.m | Open acknowledgements via file URL (`openURL:`) instead of `openFile:`. |\r\n| Cakebrew/Frameworks/Sparkle.framework/Versions/A/Resources/SUModelTranslation.plist | Remove vendored Sparkle resource. |\r\n| Cakebrew/Frameworks/Sparkle.framework/Versions/A/Resources/ReleaseNotesColorStyle.css | Remove vendored Sparkle resource. |\r\n| Cakebrew/Frameworks/Sparkle.framework/Versions/A/Resources/Info.plist | Remove vendored Sparkle resource. |\r\n| Cakebrew/Frameworks/Sparkle.framework/Versions/A/Resources/he.lproj/SUUpdateAlert.strings | Remove vendored Sparkle localization. |\r\n| Cakebrew/Frameworks/Sparkle.framework/Versions/A/Resources/he.lproj/SUAutomaticUpdateAlert.strings | Remove vendored Sparkle localization. |\r\n| Cakebrew/Frameworks/Sparkle.framework/Versions/A/Resources/en.lproj/SUUpdatePermissionPrompt.strings | Remove vendored Sparkle localization. |\r\n| Cakebrew/Frameworks/Sparkle.framework/Versions/A/Resources/en.lproj/SUUpdateAlert.strings | Remove vendored Sparkle localization. |\r\n| Cakebrew/Frameworks/Sparkle.framework/Versions/A/Resources/en.lproj/SUAutomaticUpdateAlert.strings | Remove vendored Sparkle localization. |\r\n| Cakebrew/Frameworks/Sparkle.framework/Versions/A/Resources/cs.lproj/SUUpdatePermissionPrompt.strings | Remove vendored Sparkle localization. |\r\n| Cakebrew/Frameworks/Sparkle.framework/Versions/A/Resources/cs.lproj/SUUpdateAlert.strings | Remove vendored Sparkle localization. |\r\n| Cakebrew/Frameworks/Sparkle.framework/Versions/A/Resources/cs.lproj/SUAutomaticUpdateAlert.strings | […]

> AGENT

Copilot left 8 inline comments. Before I act, let me verify a few things — some of these suggestions are good, but a couple (like removing your `DEVELOPMENT_TEAM`) would actually hurt a personal repo. Let me check what's actually in the diff vs. pre-existing.

> TOOL

tool_use Bash
id: toolu_01M1LKiwzoFDYGYx5CaXmshj
```json
{
  "command": "echo \"==== .genkit tracked? ====\"; git ls-files .genkit; git log --oneline -- .genkit 2>/dev/null | head; echo \"==== is bundle id / dev team changed vs master? ====\"; git diff master..HEAD -- Cakebrew.xcodeproj/project.pbxproj | grep -nE \"PRODUCT_BUNDLE_IDENTIFIER|DEVELOPMENT_TEAM\" ; echo \"==== current values in project ====\"; grep -nE \"PRODUCT_BUNDLE_IDENTIFIER|DEVELOPMENT_TEAM\" Cakebrew.xcodeproj/project.pbxproj",
  "description": "Check genkit tracking and whether bundle id/team changed vs master"
}
```

> TOOL

tool_result
id: toolu_01M1LKiwzoFDYGYx5CaXmshj
```
==== .genkit tracked? ====
.genkit/traces_idx/genkit.metadata
76c5ffd Remove Sparkle.framework and fix acknowledgements URL handling
==== is bundle id / dev team changed vs master? ====
166:-				DEVELOPMENT_TEAM = R85D3K8ATT;
168:+				DEVELOPMENT_TEAM = 27ZDER873F;
184:-				PRODUCT_BUNDLE_IDENTIFIER = "com.brunophilipe.${PRODUCT_NAME:rfc1034identifier}";
185:+				PRODUCT_BUNDLE_IDENTIFIER = "com.scottdensmore.--PRODUCT-NAME-rfc1034identifier-";
186:+				"PRODUCT_BUNDLE_IDENTIFIER[sdk=macosx*]" = com.scottdensmore.Cakebrew;
197:-				DEVELOPMENT_TEAM = R85D3K8ATT;
199:+				DEVELOPMENT_TEAM = 27ZDER873F;
215:-				PRODUCT_BUNDLE_IDENTIFIER = "com.brunophilipe.${PRODUCT_NAME:rfc1034identifier}";
216:+				PRODUCT_BUNDLE_IDENTIFIER = "com.scottdensmore.--PRODUCT-NAME-rfc1034identifier-";
217:+				"PRODUCT_BUNDLE_IDENTIFIER[sdk=macosx*]" = com.scottdensmore.Cakebrew;
245:-				PRODUCT_BUNDLE_IDENTIFIER = "com.hrubasko.$(PRODUCT_NAME:rfc1034identifier)";
246:+				PRODUCT_BUNDLE_IDENTIFIER = "com.scottdensmore.--PRODUCT-NAME-rfc1034identifier-";
271:-				PRODUCT_BUNDLE_IDENTIFIER = "com.hrubasko.$(PRODUCT_NAME:rfc1034identifier)";
272:+				PRODUCT_BUNDLE_IDENTIFIER = "com.scottdensmore.--PRODUCT-NAME-rfc1034identifier-";
==== current values in project ====
1023:				DEVELOPMENT_TEAM = 27ZDER873F;
1040:				PRODUCT_BUNDLE_IDENTIFIER = "com.scottdensmore.--PRODUCT-NAME-rfc1034identifier-";
1041:				"PRODUCT_BUNDLE_IDENTIFIER[sdk=macosx*]" = com.scottdensmore.Cakebrew;
1060:				DEVELOPMENT_TEAM = 27ZDER873F;
1076:				PRODUCT_BUNDLE_IDENTIFIER = "com.scottdensmore.--PRODUCT-NAME-rfc1034identifier-";
1077:				"PRODUCT_BUNDLE_IDENTIFIER[sdk=macosx*]" = com.scottdensmore.Cakebrew;
1116:				PRODUCT_BUNDLE_IDENTIFIER = "com.scottdensmore.--PRODUCT-NAME-rfc1034identifier-";
1150:				PRODUCT_BUNDLE_IDENTIFIER = "com.scottdensmore.--PRODUCT-NAME-rfc1034identifier-";
```

> TOOL

tool_use Bash
id: toolu_01LBJdHqJi4ZLobm3m98AHFZ
```json
{
  "command": "echo \"==== master values ====\"; git show master:Cakebrew.xcodeproj/project.pbxproj | grep -nE \"PRODUCT_BUNDLE_IDENTIFIER|DEVELOPMENT_TEAM\" ; echo \"==== Check for Updates menu item in xib ====\"; grep -n \"Check for Updates\\|checkForUpdates\\|SUUpdater\\|Sparkle\" Cakebrew/Base.lproj/MainMenu.xib",
  "description": "Compare master bundle id/team values and find Check for Updates menu item"
}
```

> TOOL

tool_result
id: toolu_01LBJdHqJi4ZLobm3m98AHFZ
```
==== master values ====
1051:				DEVELOPMENT_TEAM = R85D3K8ATT;
1063:				PRODUCT_BUNDLE_IDENTIFIER = "com.brunophilipe.${PRODUCT_NAME:rfc1034identifier}";
1082:				DEVELOPMENT_TEAM = R85D3K8ATT;
1093:				PRODUCT_BUNDLE_IDENTIFIER = "com.brunophilipe.${PRODUCT_NAME:rfc1034identifier}";
1128:				PRODUCT_BUNDLE_IDENTIFIER = "com.hrubasko.$(PRODUCT_NAME:rfc1034identifier)";
1157:				PRODUCT_BUNDLE_IDENTIFIER = "com.hrubasko.$(PRODUCT_NAME:rfc1034identifier)";
==== Check for Updates menu item in xib ====
34:                            <menuItem title="Check for Updates…" id="v4F-qE-2u0">
```

> AGENT

Now I have the full context. Here's my read on the 8 comments:

- **Bundle identifier (×4)** — Real wart: your branch changed it to a mangled literal `com.scottdensmore.--PRODUCT-NAME-rfc1034identifier-`. The macOS app is saved by an SDK override (`com.scottdensmore.Cakebrew`), but the test target has no override. Worth cleaning up.
- **`DEVELOPMENT_TEAM` (×1)** — Copilot is **wrong here** for your fork: you changed it from brunophilipe's team to *your* team (`27ZDER873F`). Removing it would break your local signing. I'll leave it.
- **Dangling "Check for Updates…" menu item (×1)** — Valid; Sparkle is gone.
- **`.genkit/` committed (×1)** — Valid; got committed accidentally in the Sparkle commit. Should be gitignored.
- **Typo `instaledFormulaeSidebarItem` (×1)** — Valid, in my migrated code. Easy fix.

Let me inspect the menu item and gitignore before editing.

> TOOL

tool_use Read
id: toolu_01P9EwyPUwcJqZM7asZ2CHXc
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/Base.lproj/MainMenu.xib",
  "offset": 28,
  "limit": 22
}
```

> TOOL

tool_result
id: toolu_01P9EwyPUwcJqZM7asZ2CHXc
```
28	                                <modifierMask key="keyEquivalentModifierMask" command="YES"/>
29	                            </menuItem>
30	                            <menuItem title="Preferences…" hidden="YES" enabled="NO" keyEquivalent="," id="129"/>
31	                            <menuItem isSeparatorItem="YES" id="143">
32	                                <modifierMask key="keyEquivalentModifierMask" command="YES"/>
33	                            </menuItem>
34	                            <menuItem title="Check for Updates…" id="v4F-qE-2u0">
35	                                <modifierMask key="keyEquivalentModifierMask"/>
36	                            </menuItem>
37	                            <menuItem title="Visit Website" id="seZ-rp-Anf">
38	                                <modifierMask key="keyEquivalentModifierMask"/>
39	                                <connections>
40	                                    <action selector="openWebsite:" target="494" id="P8s-SO-M1k"/>
41	                                </connections>
42	                            </menuItem>
43	                            <menuItem isSeparatorItem="YES" id="149">
44	                                <modifierMask key="keyEquivalentModifierMask" command="YES"/>
45	                            </menuItem>
46	                            <menuItem title="Services" id="131">
47	                                <menu key="submenu" title="Services" systemMenu="services" id="130"/>
48	                            </menuItem>
49	                            <menuItem isSeparatorItem="YES" id="144">
```

> TOOL

tool_use Bash
id: toolu_018KF4dxyUmX8BhN1hDVoW7t
```json
{
  "command": "echo \"==== .gitignore ====\"; cat .gitignore 2>/dev/null || echo \"(no .gitignore)\"; echo \"==== test target bundle id context (Debug ~1110-1120, Release ~1145-1155) ====\"; sed -n '1108,1120p;1145,1155p' Cakebrew.xcodeproj/project.pbxproj",
  "description": "Read gitignore and test target bundle id context"
}
```

> TOOL

tool_result
id: toolu_018KF4dxyUmX8BhN1hDVoW7t
```
==== .gitignore ====
# Created by https://www.gitignore.io

### Xcode ###
build/
*.pbxuser
!default.pbxuser
*.mode1v3
!default.mode1v3
*.mode2v3
!default.mode2v3
*.perspectivev3
!default.perspectivev3
xcuserdata
*.xccheckout
*.moved-aside
DerivedData
*.xcuserstate


### OSX ###
.DS_Store
.AppleDouble
.LSOverride

# Icon must end with two \r
Icon


# Thumbnails
._*

# Files that might appear on external disk
.Spotlight-V100
.Trashes

# Directories potentially created on remote AFP share
.AppleDB
.AppleDesktop
Network Trash Folder
Temporary Items
.apdisk


### AppCode ###
# Covers JetBrains IDEs: IntelliJ, RubyMine, PhpStorm, AppCode, PyCharm

*.iml

## Directory-based project format:
.idea/
# if you remove the above rule, at least ignore the following:

# User-specific stuff:
# .idea/workspace.xml
# .idea/tasks.xml
# .idea/dictionaries

# Sensitive or high-churn files:
# .idea/dataSources.ids
# .idea/dataSources.xml
# .idea/sqlDataSources.xml
# .idea/dynamic.xml
# .idea/uiDesigner.xml

# Gradle:
# .idea/gradle.xml
# .idea/libraries

# Mongo Explorer plugin:
# .idea/mongoSettings.xml

## File-based project format:
*.ipr
*.iws

## Plugin-specific files:

# IntelliJ
out/

# mpeltonen/sbt-idea plugin
.idea_modules/

# JIRA plugin
atlassian-ide-plugin.xml

# Crashlytics plugin (for Android Studio and IntelliJ)
com_crashlytics_export_strings.xml
crashlytics.properties
crashlytics-build.properties

==== test target bundle id context (Debug ~1110-1120, Release ~1145-1155) ====
				INFOPLIST_FILE = CakebrewTests/Info.plist;
				LD_RUNPATH_SEARCH_PATHS = (
					"$(inherited)",
					"@executable_path/../Frameworks",
					"@loader_path/../Frameworks",
				);
				MACOSX_DEPLOYMENT_TARGET = 26.0;
				MTL_ENABLE_DEBUG_INFO = YES;
				PRODUCT_BUNDLE_IDENTIFIER = "com.scottdensmore.--PRODUCT-NAME-rfc1034identifier-";
				PRODUCT_NAME = […]

> AGENT

Now I'll make the safe fixes. Starting with the typo, the dead menu item, and the gitignore.

> TOOL

tool_use Edit
id: toolu_01C8wXDZk9WcAFv8UcMthjcb
```json
{
  "replace_all": true,
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/Controllers/BPSideBarController.m",
  "old_string": "instaledFormulaeSidebarItem",
  "new_string": "installedFormulaeSidebarItem"
}
```

> TOOL

tool_result
id: toolu_01C8wXDZk9WcAFv8UcMthjcb
```
The file /home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/Controllers/BPSideBarController.m has been updated. All occurrences were successfully replaced. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_018Tm2kzhtSBoGqXo2Rv92Ha
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/Base.lproj/MainMenu.xib",
  "old_string": "                            <menuItem title=\"Check for Updates…\" id=\"v4F-qE-2u0\">\n                                <modifierMask key=\"keyEquivalentModifierMask\"/>\n                            </menuItem>\n                            <menuItem title=\"Visit Website\" id=\"seZ-rp-Anf\">",
  "new_string": "                            <menuItem title=\"Visit Website\" id=\"seZ-rp-Anf\">"
}
```

> TOOL

tool_result
id: toolu_018Tm2kzhtSBoGqXo2Rv92Ha
```
The file /home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/Base.lproj/MainMenu.xib has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_result ERROR
id: toolu_01GRQ8MUwUPuDPmrafRHFhau
```
<tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
```

> TOOL

tool_use Edit
id: toolu_01GRQ8MUwUPuDPmrafRHFhau
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/.gitignore",
  "old_string": "DerivedData\n*.xcuserstate",
  "new_string": "DerivedData\n*.xcuserstate\n\n### Genkit ###\n.genkit/"
}
```

> AGENT

The `.gitignore` edit needs a Read first. Let me read it and the exact pbxproj bundle-id lines.

> TOOL

tool_use Read
id: toolu_01UK8haSsn9esMNWMHNCPzfc
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/.gitignore",
  "offset": 1,
  "limit": 22
}
```

> TOOL

tool_result
id: toolu_01UK8haSsn9esMNWMHNCPzfc
```
1	# Created by https://www.gitignore.io
2	
3	### Xcode ###
4	build/
5	*.pbxuser
6	!default.pbxuser
7	*.mode1v3
8	!default.mode1v3
9	*.mode2v3
10	!default.mode2v3
11	*.perspectivev3
12	!default.perspectivev3
13	xcuserdata
14	*.xccheckout
15	*.moved-aside
16	DerivedData
17	*.xcuserstate
18	
19	
20	### OSX ###
21	.DS_Store
22	.AppleDouble
```

> TOOL

tool_use Read
id: toolu_01CK9crRHVp2HQAipWKxaKuF
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcodeproj/project.pbxproj",
  "offset": 1039,
  "limit": 4
}
```

> TOOL

tool_result
id: toolu_01CK9crRHVp2HQAipWKxaKuF
```
1039					ONLY_ACTIVE_ARCH = NO;
1040					PRODUCT_BUNDLE_IDENTIFIER = "com.scottdensmore.--PRODUCT-NAME-rfc1034identifier-";
1041					"PRODUCT_BUNDLE_IDENTIFIER[sdk=macosx*]" = com.scottdensmore.Cakebrew;
1042					PRODUCT_NAME = Cakebrew;
```

> AGENT

Now the gitignore and the bundle-identifier cleanup. First the gitignore and the app target (two-line pattern → one stable line).

> TOOL

tool_use Edit
id: toolu_016dDGLztYMVE37UgeyKjswk
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/.gitignore",
  "old_string": "DerivedData\n*.xcuserstate\n\n\n### OSX ###",
  "new_string": "DerivedData\n*.xcuserstate\n\n\n### Genkit ###\n.genkit/\n\n\n### OSX ###"
}
```

> TOOL

tool_result
id: toolu_016dDGLztYMVE37UgeyKjswk
```
The file /home/<USER>/Developer/scottdensmore/cakebrew/.gitignore has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_015psRwpaNndLGSVZFnmGP9f
```json
{
  "replace_all": true,
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcodeproj/project.pbxproj",
  "old_string": "\t\t\t\tPRODUCT_BUNDLE_IDENTIFIER = \"com.scottdensmore.--PRODUCT-NAME-rfc1034identifier-\";\n\t\t\t\t\"PRODUCT_BUNDLE_IDENTIFIER[sdk=macosx*]\" = com.scottdensmore.Cakebrew;\n\t\t\t\tPRODUCT_NAME = Cakebrew;",
  "new_string": "\t\t\t\tPRODUCT_BUNDLE_IDENTIFIER = com.scottdensmore.Cakebrew;\n\t\t\t\tPRODUCT_NAME = Cakebrew;"
}
```

> TOOL

tool_result
id: toolu_015psRwpaNndLGSVZFnmGP9f
```
The file /home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcodeproj/project.pbxproj has been updated. All occurrences were successfully replaced. (file state is current in your context — no need to Read it back)
```

> AGENT

Now the test target's bundle identifier (the two standalone occurrences followed by `$(TARGET_NAME)`).

> TOOL

tool_use Edit
id: toolu_01FnzSURdSfdSWwZyJNnpJcd
```json
{
  "replace_all": true,
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcodeproj/project.pbxproj",
  "old_string": "\t\t\t\tPRODUCT_BUNDLE_IDENTIFIER = \"com.scottdensmore.--PRODUCT-NAME-rfc1034identifier-\";\n\t\t\t\tPRODUCT_NAME = \"$(TARGET_NAME)\";",
  "new_string": "\t\t\t\tPRODUCT_BUNDLE_IDENTIFIER = com.scottdensmore.CakebrewTests;\n\t\t\t\tPRODUCT_NAME = \"$(TARGET_NAME)\";"
}
```

> TOOL

tool_result
id: toolu_01FnzSURdSfdSWwZyJNnpJcd
```
The file /home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcodeproj/project.pbxproj has been updated. All occurrences were successfully replaced. (file state is current in your context — no need to Read it back)
```

> AGENT

Now untrack the genkit metadata file and verify all bundle-id references are clean.

> TOOL

tool_use Bash
id: toolu_01PAdijxjr9hNDLtVcAUwbm7
```json
{
  "command": "git rm --cached .genkit/traces_idx/genkit.metadata 2>&1; echo \"==== remaining mangled ids (should be none) ====\"; grep -n \"PRODUCT-NAME-rfc1034\\|sdk=macosx\" Cakebrew.xcodeproj/project.pbxproj || echo \"none\"; echo \"==== current bundle ids ====\"; grep -n \"PRODUCT_BUNDLE_IDENTIFIER\" Cakebrew.xcodeproj/project.pbxproj",
  "description": "Untrack genkit file and verify bundle id cleanup"
}
```

> TOOL

tool_result
id: toolu_01PAdijxjr9hNDLtVcAUwbm7
```
rm '.genkit/traces_idx/genkit.metadata'
==== remaining mangled ids (should be none) ====
none
==== current bundle ids ====
1040:				PRODUCT_BUNDLE_IDENTIFIER = com.scottdensmore.Cakebrew;
1075:				PRODUCT_BUNDLE_IDENTIFIER = com.scottdensmore.Cakebrew;
1114:				PRODUCT_BUNDLE_IDENTIFIER = com.scottdensmore.CakebrewTests;
1148:				PRODUCT_BUNDLE_IDENTIFIER = com.scottdensmore.CakebrewTests;
```

> AGENT

All four bundle IDs are clean and the genkit file is untracked. Let me rebuild to confirm the project still compiles and signs after the bundle-ID and menu changes.

> TOOL

tool_use Bash
id: toolu_01HKZx5aJSn1GA1jFeFi5k93
```json
{
  "command": "xcodebuild -workspace Cakebrew.xcworkspace -scheme Cakebrew -configuration Debug -destination 'platform=macOS' build 2>&1 | grep -E \"error:|warning: .*BPSideBar|BUILD SUCCEEDED|BUILD FAILED|CodeSign|PRODUCT_BUNDLE\" | tail -20",
  "description": "Rebuild to confirm success after fixes",
  "timeout": 420000
}
```

> TOOL

tool_result
id: toolu_01HKZx5aJSn1GA1jFeFi5k93
```
CodeSign /home/<USER>/Library/Developer/Xcode/DerivedData/Cakebrew-ejkvoljwklzjefduqadkgzlgzyoq/Build/Products/Debug/CakebrewTests.xctest (in target 'CakebrewTests' from project 'Cakebrew')
CodeSign /home/<USER>/Library/Developer/Xcode/DerivedData/Cakebrew-ejkvoljwklzjefduqadkgzlgzyoq/Build/Products/Debug/Cakebrew.app (in target 'Cakebrew' from project 'Cakebrew')
** BUILD SUCCEEDED ** [5.230 sec]
```

> AGENT

Build succeeds and both targets sign with the clean bundle IDs. Let me commit and push the review fixes.

> TOOL

tool_use Bash
id: toolu_01CL7RvkkVf13WgWcWptXWEg
```json
{
  "command": "git status --short; echo \"====\"; git add .gitignore .genkit/traces_idx/genkit.metadata Cakebrew.xcodeproj/project.pbxproj Cakebrew/Base.lproj/MainMenu.xib Cakebrew/Controllers/BPSideBarController.m && git commit -m \"$(cat <<'EOF'\nAddress PR review: clean bundle ids, drop dead update menu, fix typo\n\n- Replace the mangled placeholder PRODUCT_BUNDLE_IDENTIFIER with stable\n  ids (com.scottdensmore.Cakebrew / .CakebrewTests) and remove the now\n  redundant macOS SDK override.\n- Remove the orphaned \"Check for Updates…\" menu item left behind after\n  Sparkle was removed.\n- Stop tracking generated .genkit/ tooling metadata and gitignore it.\n- Fix misspelled installedFormulaeSidebarItem property.\n\nCo-Authored-By: Claude Opus 4.7 (1M context) <<REDACTED_EMAIL>>\nEOF\n)\" && git push 2>&1 | tail -4",
  "description": "Commit and push the review fixes"
}
```

> TOOL

tool_result ERROR
id: toolu_01CL7RvkkVf13WgWcWptXWEg
```
Exit code 1
D  .genkit/traces_idx/genkit.metadata
 M .gitignore
 M Cakebrew.xcodeproj/project.pbxproj
 M Cakebrew/Base.lproj/MainMenu.xib
 M Cakebrew/Controllers/BPSideBarController.m
====
The following paths are ignored by one of your .gitignore files:
.genkit
hint: Use -f if you really want to add them.
hint: Disable this message with "git config set advice.addIgnoredFile false"
```

> AGENT

The genkit deletion is already staged (from `git rm --cached`); I just don't need to re-add the now-ignored path. Let me stage the rest and commit.

> TOOL

tool_use Bash
id: toolu_011TpG7yPUNyZYmUNRUkB7dg
```json
{
  "command": "git add .gitignore Cakebrew.xcodeproj/project.pbxproj Cakebrew/Base.lproj/MainMenu.xib Cakebrew/Controllers/BPSideBarController.m && git commit -m \"$(cat <<'EOF'\nAddress PR review: clean bundle ids, drop dead update menu, fix typo\n\n- Replace the mangled placeholder PRODUCT_BUNDLE_IDENTIFIER with stable\n  ids (com.scottdensmore.Cakebrew / .CakebrewTests) and remove the now\n  redundant macOS SDK override.\n- Remove the orphaned \"Check for Updates…\" menu item left behind after\n  Sparkle was removed.\n- Stop tracking generated .genkit/ tooling metadata and gitignore it.\n- Fix misspelled installedFormulaeSidebarItem property.\n\nCo-Authored-By: Claude Opus 4.7 (1M context) <<REDACTED_EMAIL>>\nEOF\n)\" && git push 2>&1 | tail -4",
  "description": "Commit the four modified files plus staged deletion and push"
}
```

> TOOL

tool_result
id: toolu_011TpG7yPUNyZYmUNRUkB7dg
```
[modernize-macos26 5e89ec8] Address PR review: clean bundle ids, drop dead update menu, fix typo
 5 files changed, 13 insertions(+), 15 deletions(-)
 delete mode 100644 .genkit/traces_idx/genkit.metadata
To https://github.com/scottdensmore/Cakebrew.git
   952d98a..5e89ec8  modernize-macos26 -> modernize-macos26
```

> AGENT

Pushed. Now I'll reply to each Copilot thread documenting the resolution (and noting why I'm keeping `DEVELOPMENT_TEAM`), then mark the threads resolved. Let me fetch the comment and thread IDs.

> TOOL

tool_use Bash
id: toolu_01JRmRqUBYQcC6RJPNLWoGDp
```json
{
  "command": "gh api graphql -f query='\nquery {\n  repository(owner: \"scottdensmore\", name: \"Cakebrew\") {\n    pullRequest(number: 1) {\n      reviewThreads(first: 50) {\n        nodes {\n          id\n          isResolved\n          comments(first: 1) {\n            nodes { databaseId path originalLine body }\n          }\n        }\n      }\n    }\n  }\n}' --jq '.data.repository.pullRequest.reviewThreads.nodes[] | {threadId: .id, resolved: .isResolved, commentId: .comments.nodes[0].databaseId, path: .comments.nodes[0].path, line: .comments.nodes[0].originalLine, snippet: (.comments.nodes[0].body[0:60])}'",
  "description": "Fetch review thread IDs and comment ids"
}
```

> TOOL

tool_result
id: toolu_01JRmRqUBYQcC6RJPNLWoGDp
```
{"commentId":3300285266,"line":1041,"path":"Cakebrew.xcodeproj/project.pbxproj","resolved":false,"snippet":"`PRODUCT_BUNDLE_IDENTIFIER` is set to a placeholder-like val","threadId":"PRRT_kwDOA4x9PM6EpA3-"}
{"commentId":3300285280,"line":1024,"path":"Cakebrew.xcodeproj/project.pbxproj","resolved":false,"snippet":"The project file hard-codes a `DEVELOPMENT_TEAM` value. This","threadId":"PRRT_kwDOA4x9PM6EpA4J"}
{"commentId":3300285285,"line":1077,"path":"Cakebrew.xcodeproj/project.pbxproj","resolved":false,"snippet":"Same as Debug: Release configuration sets `PRODUCT_BUNDLE_ID","threadId":"PRRT_kwDOA4x9PM6EpA4M"}
{"commentId":3300285296,"line":1116,"path":"Cakebrew.xcodeproj/project.pbxproj","resolved":false,"snippet":"CakebrewTests target uses the same placeholder-like `PRODUCT","threadId":"PRRT_kwDOA4x9PM6EpA4V"}
{"commentId":3300285304,"line":36,"path":"Cakebrew/Base.lproj/MainMenu.xib","resolved":false,"snippet":"The \"Check for Updates…\" menu item no longer has an action/t","threadId":"PRRT_kwDOA4x9PM6EpA4a"}
{"commentId":3300285317,"line":1,"path":".genkit/traces_idx/genkit.metadata","resolved":false,"snippet":"This looks like generated tooling metadata (Genkit traces in","threadId":"PRRT_kwDOA4x9PM6EpA4j"}
{"commentId":3300285335,"line":143,"path":"Cakebrew/Controllers/BPSideBarController.m","resolved":false,"snippet":"Typo in the property name `instaledFormulaeSidebarItem` (mis","threadId":"PRRT_kwDOA4x9PM6EpA4x"}
{"commentId":3300285352,"line":1150,"path":"Cakebrew.xcodeproj/project.pbxproj","resolved":false,"snippet":"CakebrewTests Release configuration also uses the placeholde","threadId":"PRRT_kwDOA4x9PM6EpA4_"}
```

> AGENT

All 8 threads mapped. I'll reply to each thread documenting the resolution.

> TOOL

tool_use Bash
id: toolu_01AbPZC1SAwKeiMf4PMZVj9w
```json
{
  "command": "R=\"repos/scottdensmore/Cakebrew/pulls/1/comments\"\ngh api $R -F in_reply_to=3300285266 -f body=\"Cleaned up in 5e89ec8 — the app's base \\`PRODUCT_BUNDLE_IDENTIFIER\\` is now the stable \\`com.scottdensmore.Cakebrew\\` and the redundant \\`[sdk=macosx*]\\` override was removed.\" --jq .id\ngh api $R -F in_reply_to=3300285285 -f body=\"Fixed in 5e89ec8 — Release now uses the stable \\`com.scottdensmore.Cakebrew\\` with the redundant SDK override removed.\" --jq .id\ngh api $R -F in_reply_to=3300285296 -f body=\"Fixed in 5e89ec8 — the test target now uses a stable \\`com.scottdensmore.CakebrewTests\\` identifier.\" --jq .id\ngh api $R -F in_reply_to=3300285352 -f body=\"Fixed in 5e89ec8 — Release test config now uses the stable \\`com.scottdensmore.CakebrewTests\\` identifier.\" --jq .id\ngh api $R -F in_reply_to=3300285304 -f body=\"Removed in 5e89ec8 — Sparkle was removed and there's no replacement updater, so the orphaned \\\"Check for Updates…\\\" item is gone.\" --jq .id\ngh api $R -F in_reply_to=3300285317 -f body=\"Fixed in 5e89ec8 — removed from version control and added \\`.genkit/\\` to .gitignore.\" --jq .id\ngh api $R -F in_reply_to=3300285335 -f body=\"Fixed in 5e89ec8 — renamed to \\`installedFormulaeSidebarItem\\`.\" --jq .id\ngh api $R -F in_reply_to=3300285280 -f body=\"Intentionally leaving this as-is: this is a personal fork and \\`27ZDER873F\\` is the maintainer's own Apple Developer team (changed from the upstream team specifically so the app signs locally). Removing it would break local […]

> TOOL

tool_result
id: toolu_01AbPZC1SAwKeiMf4PMZVj9w
```
3300353134
3300353168
3300353203
3300353254
3300353299
3300353327
3300353369
3300353406
```

> AGENT

Replies posted. Now I'll mark the seven addressed threads resolved, leaving only the `DEVELOPMENT_TEAM` thread open for your call.

> TOOL

tool_use Bash
id: toolu_01ABBE8TPBNA9o5rssmRBYS3
```json
{
  "command": "M='mutation($id:ID!){resolveReviewThread(input:{threadId:$id}){thread{isResolved}}}'\nfor T in PRRT_kwDOA4x9PM6EpA3- PRRT_kwDOA4x9PM6EpA4M PRRT_kwDOA4x9PM6EpA4V PRRT_kwDOA4x9PM6EpA4_ PRRT_kwDOA4x9PM6EpA4a PRRT_kwDOA4x9PM6EpA4j PRRT_kwDOA4x9PM6EpA4x; do\n  echo -n \"$T -> \"; gh api graphql -f query=\"$M\" -f id=\"$T\" --jq '.data.resolveReviewThread.thread.isResolved'\ndone",
  "description": "Resolve the seven addressed review threads"
}
```

> TOOL

tool_result
id: toolu_01ABBE8TPBNA9o5rssmRBYS3
```
PRRT_kwDOA4x9PM6EpA3- -> true
PRRT_kwDOA4x9PM6EpA4M -> true
PRRT_kwDOA4x9PM6EpA4V -> true
PRRT_kwDOA4x9PM6EpA4_ -> true
PRRT_kwDOA4x9PM6EpA4a -> true
PRRT_kwDOA4x9PM6EpA4j -> true
PRRT_kwDOA4x9PM6EpA4x -> true
```

> AGENT

Done. Here's how I handled Copilot's 8 comments on [PR #1](https://github.com/scottdensmore/Cakebrew/pull/1):

**Fixed and resolved (7 threads), pushed as `5e89ec8`:**
- **Bundle identifier (×4)** — your branch had a mangled `com.scottdensmore.--PRODUCT-NAME-rfc1034identifier-`. Set stable IDs: `com.scottdensmore.Cakebrew` (app) and `com.scottdensmore.CakebrewTests` (tests), and dropped the now-redundant `[sdk=macosx*]` override. The app's resolved macOS ID is unchanged.
- **"Check for Updates…" menu item** — removed; it was orphaned after Sparkle's removal with no replacement updater.
- **`.genkit/` metadata** — untracked and added to `.gitignore`.
- **Typo** — `instaledFormulaeSidebarItem` → `installedFormulaeSidebarItem`.

**Declined (1 thread, left open for you):**
- **`DEVELOPMENT_TEAM`** — Copilot suggested removing it, but `27ZDER873F` is *your* Apple Developer team (you changed it from brunophilipe's upstream team so the app signs on your machine). Removing it would break local signing. I replied on the thread explaining and left it unresolved so you can make the final call.

Rebuild after the changes: **BUILD SUCCEEDED**, both targets sign cleanly.

The PR is still open and unmerged, ready for your review. Want me to do anything about that one `DEVELOPMENT_TEAM` thread, or leave it?

> DEVELOPER

check the pr and see if there are any comments and if so address them

> AGENT

I'll check the PR for any new comments since the last round.

> TOOL

tool_use Bash
id: toolu_01QFD5W829ZoEzoDrR3NvLAf
```json
{
  "command": "echo \"==== unresolved review threads ====\"; gh api graphql -f query='\nquery {\n  repository(owner: \"scottdensmore\", name: \"Cakebrew\") {\n    pullRequest(number: 1) {\n      reviewThreads(first: 50) {\n        nodes {\n          id\n          isResolved\n          isOutdated\n          comments(first: 10) {\n            nodes { databaseId author { login } path originalLine createdAt body }\n          }\n        }\n      }\n    }\n  }\n}' --jq '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved==false) | {threadId:.id, outdated:.isOutdated, comments:[.comments.nodes[]|{id:.databaseId, user:.author.login, path:.path, line:.originalLine, created:.createdAt, body:.body}]}'",
  "description": "Fetch unresolved review threads with full comment chains"
}
```

> TOOL

tool_use Bash
id: toolu_01XEZQWbJFyMwvFsqgWkdHCg
```json
{
  "command": "echo \"==== reviews ====\"; gh pr view 1 --repo scottdensmore/Cakebrew --json reviews --jq '.reviews[] | {user:.author.login, state:.state, at:.submittedAt, body:(.body[0:200])}'; echo \"==== issue comments ====\"; gh api repos/scottdensmore/Cakebrew/issues/1/comments --jq '.[] | {user:.user.login, at:.created_at, body:.body}'; echo \"==== latest commit on PR ====\"; gh pr view 1 --repo scottdensmore/Cakebrew --json commits --jq '.commits[-1].oid'",
  "description": "Fetch PR reviews, issue comments, and latest commit"
}
```

> TOOL

tool_result
id: toolu_01QFD5W829ZoEzoDrR3NvLAf
```
==== unresolved review threads ====
{"comments":[{"body":"The project file hard-codes a `DEVELOPMENT_TEAM` value. This is environment/user-specific and tends to cause signing problems for other contributors/CI; consider removing it (let Xcode manage per-user signing) or restoring the previous team setting if it was intentionally shared.","created":"2026-05-25T23:16:10Z","id":3300285280,"line":1024,"path":"Cakebrew.xcodeproj/project.pbxproj","user":"copilot-pull-request-reviewer"},{"body":"Intentionally leaving this as-is: this is a personal fork and `27ZDER873F` is the maintainer's own Apple Developer team (changed from the upstream team specifically so the app signs locally). Removing it would break local signing, so this is the desired value rather than a mistake.","created":"2026-05-25T23:46:02Z","id":3300353406,"line":1024,"path":"Cakebrew.xcodeproj/project.pbxproj","user":"scottdensmore"}],"outdated":false,"threadId":"PRRT_kwDOA4x9PM6EpA4J"}
```

> TOOL

tool_result
id: toolu_01XEZQWbJFyMwvFsqgWkdHCg
```
==== reviews ====
{"at":"2026-05-25T23:16:12Z","body":"## Pull request overview\n\nModernizes Cakebrew’s macOS integration by removing legacy vendored dependencies (Sparkle, PXSourceList) and reworking the sidebar to use native AppKit (`NSOutlineView`), alo","state":"COMMENTED","user":"copilot-pull-request-reviewer"}
{"at":"2026-05-25T23:45:54Z","body":"","state":"COMMENTED","user":"scottdensmore"}
{"at":"2026-05-25T23:45:55Z","body":"","state":"COMMENTED","user":"scottdensmore"}
{"at":"2026-05-25T23:45:56Z","body":"","state":"COMMENTED","user":"scottdensmore"}
{"at":"2026-05-25T23:45:58Z","body":"","state":"COMMENTED","user":"scottdensmore"}
{"at":"2026-05-25T23:45:59Z","body":"","state":"COMMENTED","user":"scottdensmore"}
{"at":"2026-05-25T23:46:00Z","body":"","state":"COMMENTED","user":"scottdensmore"}
{"at":"2026-05-25T23:46:01Z","body":"","state":"COMMENTED","user":"scottdensmore"}
{"at":"2026-05-25T23:46:02Z","body":"","state":"COMMENTED","user":"scottdensmore"}
==== issue comments ====
==== latest commit on PR ====
5e89ec84a4d73d7f7e6f6458c47b64195f42f9c1
```

> AGENT

I checked — there are **no new comments** since the last round. Here's the current state of [PR #1](https://github.com/scottdensmore/Cakebrew/pull/1):

- **Copilot has not re-reviewed** the latest commit (`5e89ec8`). Its only review is the original one on `952d98a`, whose 7 actionable findings I already fixed and resolved.
- **One thread remains open**: the `DEVELOPMENT_TEAM` one. It's not new — it already has my reply explaining that `27ZDER873F` is intentionally your own signing team (removing it would break local signing). I left it unresolved on purpose so it's your call.
- No new issue comments. (The eight empty "COMMENTED" review events from `scottdensmore` are just the wrappers around the inline replies I posted last round — not new feedback.)

So nothing new to address. Two things you might want:

1. **Re-request a Copilot review** on `5e89ec8` so it can confirm the earlier issues are cleared — want me to trigger that?
2. **Resolve or keep** the `DEVELOPMENT_TEAM` thread — I can mark it resolved if you agree with keeping your team ID, or leave it open.

And the PR is still unmerged whenever you're ready to squash-merge.

> DEVELOPER

Yea trigger it

> AGENT

I'll re-request a Copilot review on the latest commit.

> TOOL

tool_use Bash
id: toolu_01CXVTa9PgK5v5q3jd4cy49z
```json
{
  "command": "gh api repos/scottdensmore/Cakebrew/pulls/1/requested_reviewers -X POST -f \"reviewers[]=copilot-pull-request-reviewer\" 2>&1 | head -20",
  "description": "Request Copilot re-review via reviewers endpoint"
}
```

> TOOL

tool_result
id: toolu_01CXVTa9PgK5v5q3jd4cy49z
```
{"message":"Reviews may only be requested from collaborators. One or more of the users or teams you specified is not a collaborator of the scottdensmore/Cakebrew repository.","documentation_url":"https://docs.github.com/rest/pulls/review-requests#request-reviewers-for-a-pull-request","status":"422"}gh: Reviews may only be requested from collaborators. One or more of the users or teams you specified is not a collaborator of the scottdensmore/Cakebrew repository. (HTTP 422)
```

> AGENT

The Copilot bot can't be requested as a regular collaborator. I need its bot node ID and the GraphQL `requestReviews` mutation. Let me grab the bot's ID from its existing review, plus the PR's GraphQL node ID.

> TOOL

tool_use Bash
id: toolu_01WYGUbVDsChciu2qQ9NpGbK
```json
{
  "command": "gh api graphql -f query='\nquery {\n  repository(owner: \"scottdensmore\", name: \"Cakebrew\") {\n    pullRequest(number: 1) {\n      id\n      reviews(first: 1) { nodes { author { login __typename ... on Bot { id } ... on User { id } } } }\n    }\n  }\n}'",
  "description": "Get PR node id and Copilot bot author id"
}
```

> TOOL

tool_result
id: toolu_01WYGUbVDsChciu2qQ9NpGbK
```
{"data":{"repository":{"pullRequest":{"id":"PR_kwDOA4x9PM7fMhSD","reviews":{"nodes":[{"author":{"login":"copilot-pull-request-reviewer","__typename":"Bot","id":"BOT_kgDOCnlnWA"}}]}}}}}
```

> AGENT

I have the PR node ID and Copilot's bot ID. Triggering the re-review via the `requestReviews` mutation.

> TOOL

tool_use Bash
id: toolu_019HcXR2QL2ewoPV8LwtweZg
```json
{
  "command": "gh api graphql -f query='\nmutation {\n  requestReviews(input: {pullRequestId: \"PR_kwDOA4x9PM7fMhSD\", botIds: [\"BOT_kgDOCnlnWA\"], union: true}) {\n    pullRequest {\n      reviewRequests(first: 10) { nodes { requestedReviewer { __typename ... on Bot { login } } } }\n    }\n  }\n}'",
  "description": "Request a fresh Copilot review on the PR"
}
```

> TOOL

tool_result
id: toolu_019HcXR2QL2ewoPV8LwtweZg
```
{"data":{"requestReviews":{"pullRequest":{"reviewRequests":{"nodes":[{"requestedReviewer":{"__typename":"Bot","login":"copilot-pull-request-reviewer"}}]}}}}}
```

> AGENT

Triggered — Copilot is now a requested reviewer on the PR. Its review usually lands within a few minutes. Let me check whether it's posted yet.

> TOOL

tool_use Bash
id: toolu_016ospPm4cLYDhkmdT3QgZRj
```json
{
  "command": "until [ \"$(gh pr view 1 --repo scottdensmore/Cakebrew --json reviews --jq '[.reviews[] | select(.author.login==\"copilot-pull-request-reviewer\")] | length')\" -ge 2 ]; do sleep 15; done; echo \"Copilot re-review has landed\"",
  "description": "Poll until Copilot posts its second review",
  "run_in_background": true
}
```

> TOOL

tool_result
id: toolu_016ospPm4cLYDhkmdT3QgZRj
```
Command running in background with ID: b41jnv59q. Output is being written to: /private/tmp/claude-501/-Users-scottdensmore-Developer-scottdensmore-cakebrew/86f7230f-16a2-4201-9dae-105c1789c2c6/tasks/b41jnv59q.output. You will be notified when it completes. To check interim output, use Read on that file path.
```

> AGENT

Done — Copilot's re-review is requested and I've set a background watcher that'll notify me the moment the new review lands. I'll review whatever it finds and address anything actionable, same as before. Sit tight; I'll report back when it posts.

> AGENT

The re-review has landed. Let me pull its findings.

> TOOL

tool_use Bash
id: toolu_01WiG58oTfEp52dGTh8ct5rP
```json
{
  "command": "echo \"==== Copilot reviews (chronological) ====\"; gh pr view 1 --repo scottdensmore/Cakebrew --json reviews --jq '.reviews[] | select(.author.login==\"copilot-pull-request-reviewer\") | {at:.submittedAt, state:.state, body:(.body[0:400])}'; echo; echo \"==== unresolved review threads ====\"; gh api graphql -f query='\nquery {\n  repository(owner: \"scottdensmore\", name: \"Cakebrew\") {\n    pullRequest(number: 1) {\n      reviewThreads(first: 50) {\n        nodes {\n          id isResolved isOutdated\n          comments(first: 10) { nodes { databaseId author { login } path originalLine createdAt body } }\n        }\n      }\n    }\n  }\n}' --jq '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved==false) | {threadId:.id, outdated:.isOutdated, comments:[.comments.nodes[]|{id:.databaseId, user:.author.login, path:.path, line:.originalLine, created:.createdAt, body:.body}]}'",
  "description": "Fetch new Copilot review and unresolved threads"
}
```

> TOOL

tool_result
id: toolu_01WiG58oTfEp52dGTh8ct5rP
```
==== Copilot reviews (chronological) ====
{"at":"2026-05-25T23:16:12Z","body":"## Pull request overview\n\nModernizes Cakebrew’s macOS integration by removing legacy vendored dependencies (Sparkle, PXSourceList) and reworking the sidebar to use native AppKit (`NSOutlineView`), along with a few related platform updates.\n\n**Changes:**\n- Remove vendored Sparkle framework files and related workspace/project wiring.\n- Remove PXSourceList dependency and migrate the sidebar UI/data s","state":"COMMENTED"}
{"at":"2026-05-26T01:48:47Z","body":"## Pull request overview\n\nCopilot reviewed 56 out of 215 changed files in this pull request and generated 2 comments.\n\n\u003cdetails\u003e\n\u003csummary\u003eFiles not reviewed (1)\u003c/summary\u003e\n\n* **Cakebrew.xcworkspace/contents.xcworkspacedata**: Language not supported\n\u003c/details\u003e\n\n\n\u003cdetails\u003e\n\u003csummary\u003eComments suppressed due to low confidence (1)\u003c/summary\u003e\n\n**Cakebrew/BPHomebrewManager.m:216**\n* If `archivedDataWithRoot","state":"COMMENTED"}

==== unresolved review threads ====
{"comments":[{"body":"The project file hard-codes a `DEVELOPMENT_TEAM` value. This is environment/user-specific and tends to cause signing problems for other contributors/CI; consider removing it (let Xcode manage per-user signing) or restoring the previous team setting if it was intentionally shared.","created":"2026-05-25T23:16:10Z","id":3300285280,"line":1024,"path":"Cakebrew.xcodeproj/project.pbxproj","user":"copilot-pull-request-reviewer"},{"body":"Intentionally leaving this as-is: this is a personal fork and `27ZDER873F` is the maintainer's own Apple Developer team (changed from the upstream team specifically so the app signs locally). Removing it would break local signing, so this is the desired value rather than a mistake.","created":"2026-05-25T23:46:02Z","id":3300353406,"line":1024,"path":"Cakebrew.xcodeproj/project.pbxproj","user":"scottdensmore"}],"outdated":false,"threadId":"PRRT_kwDOA4x9PM6EpA4J"}
{"comments":[{"body":"`unarchivedObjectOfClasses:fromData:error:` is missing `[NSArray class]` in the allowed classes set. The cached `kBPCacheDataKey` value is an `NSArray\u003cBPFormula *\u003e`, and `BPFormula` also encodes […]

> AGENT

The re-review found **2 new issues** (and suppressed a 3rd low-confidence one, which is actually related). Let me read the relevant code to verify both before fixing.

> TOOL

tool_use Bash
id: toolu_013JaqQ4M6TxQtnTWwn8Lvxt
```json
{
  "command": "grep -n \"unarchiv\\|archiv\\|kBPCacheDataKey\\|allowedClasses\\|NSSet\\|setWithObjects\\|setWithArray\\|loadDataFromDisk\\|saveDataToDisk\\|NSKeyedArchiver\\|NSKeyedUnarchiver\" Cakebrew/BPHomebrewManager.m",
  "description": "Locate archive/unarchive code in BPHomebrewManager"
}
```

> TOOL

tool_result
id: toolu_013JaqQ4M6TxQtnTWwn8Lvxt
```
28:NSString *const kBPCacheDataKey	= @"BPCacheDataKey";
156:				NSSet *classes = [NSSet setWithArray:@[[NSDictionary class], [NSMutableArray class], [BPFormula class], [NSString class], [NSURL class], [NSNumber class], [BPFormulaOption class]]];
157:				cacheDict = [NSKeyedUnarchiver unarchivedObjectOfClasses:classes fromData:data error:&error];
164:				cacheDict = [NSKeyedUnarchiver unarchivedObjectOfClass:[NSDictionary class] fromData:data error:&fallbackError];
169:			self.allFormulae = [cacheDict objectForKey:kBPCacheDataKey];
198:			NSDictionary *cacheDict = @{kBPCacheDataKey: self.allFormulae};
200:			NSData *cacheData = [NSKeyedArchiver archivedDataWithRootObject:cacheDict
```

> TOOL

tool_use Read
id: toolu_01E2UpG9yB2zRzx8iUtxtf4D
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/BPHomebrewManager.m",
  "offset": 140,
  "limit": 90
}
```

> TOOL

tool_result
id: toolu_01E2UpG9yB2zRzx8iUtxtf4D
```
140			if ([[NSDate date] timeIntervalSinceDate:storageDate] <= 3600*24)
141			{
142				shouldLoadCache = YES;
143			}
144		}
145		
146		if (shouldLoadCache && allFormulaeFile)
147		{
148			NSDictionary *cacheDict = nil;
149			
150			if ([[NSFileManager defaultManager] fileExistsAtPath:allFormulaeFile.relativePath])
151			{
152				NSData *data = [NSData dataWithContentsOfFile:allFormulaeFile.relativePath];
153				NSError *error = nil;
154	
155				if (@available(macOS 10.13, *)) {
156					NSSet *classes = [NSSet setWithArray:@[[NSDictionary class], [NSMutableArray class], [BPFormula class], [NSString class], [NSURL class], [NSNumber class], [BPFormulaOption class]]];
157					cacheDict = [NSKeyedUnarchiver unarchivedObjectOfClasses:classes fromData:data error:&error];
158					if (error) {
159						NSLog(@"Failed decoding data: %@", [error localizedDescription]);
160					}
161				} else {
162					// Fallback for older macOS versions
163					NSError *fallbackError = nil;
164					cacheDict = [NSKeyedUnarchiver unarchivedObjectOfClass:[NSDictionary class] fromData:data error:&fallbackError];
165					if (fallbackError) {
166						NSLog(@"Failed decoding data: %@", [fallbackError localizedDescription]);
167					}
168				}
169				self.allFormulae = [cacheDict objectForKey:kBPCacheDataKey];
170			}
171		}
172		else
173		{
174			// Delete all cache data
175			[[NSFileManager defaultManager] removeItemAtURL:allFormulaeFile error:nil];
176			[[NSUserDefaults standardUserDefaults] removeObjectForKey:kBPCacheLastUpdateKey];
177		}
178		
179		return self.allFormulae != nil;
180	}
181	
182	- (void)storeAllFormulaeCaches
183	{
184		if (self.allFormulae)
185		{
186			NSURL *cachesFolder = [BPAppDelegate urlForApplicationCachesFolder];
187			if (cachesFolder)
188			{
189				NSURL […]

> AGENT

Comment 1 is a real bug. The cache is a `NSDictionary` → `NSArray<BPFormula*>`, and `BPFormula` itself encodes an `NSArray` of options — but the allowed-classes set has `NSMutableArray`, **not** `NSArray`. Since `NSMutableArray` is a *subclass*, it doesn't permit the immutable `NSArray` containers that `NSKeyedArchiver` produces, so secure decoding fails and the cache silently never loads. Let me confirm `BPFormula`'s coding to get the complete class set.

> TOOL

tool_use Bash
id: toolu_01W3o4tSZAFeoBfHiMMk2Bd4
```json
{
  "command": "grep -n \"encodeObject\\|decodeObjectOfClass\\|decodeObjectForKey\\|initWithCoder\\|encodeWithCoder\\|@property\" Cakebrew/BPFormula.h Cakebrew/BPFormula.m Cakebrew/BPFormulaOption.h Cakebrew/BPFormulaOption.m 2>/dev/null",
  "description": "Inspect BPFormula and BPFormulaOption NSCoding and properties"
}
```

> TOOL

tool_result ERROR
id: toolu_01W3o4tSZAFeoBfHiMMk2Bd4
```
Exit code 2
```

> TOOL

tool_use Bash
id: toolu_01AeQF2nQaLecJamxNhFGR7s
```json
{
  "command": "find Cakebrew -name \"BPFormula*.m\" -o -name \"BPFormula*.h\" | head; echo \"====\"; for f in $(find Cakebrew -name \"BPFormula.m\" -o -name \"BPFormulaOption.m\"); do echo \"---- $f ----\"; grep -n \"encodeObject\\|decodeObject\\|initWithCoder\\|encodeWithCoder\" \"$f\"; done",
  "description": "Find BPFormula files and their coding methods"
}
```

> TOOL

tool_result
id: toolu_01AeQF2nQaLecJamxNhFGR7s
```
Cakebrew/BPFormulaeTableView.h
Cakebrew/BPFormulaeDataSource.h
Cakebrew/BPFormulaeTableView.m
Cakebrew/BPFormulaeDataSource.m
Cakebrew/Models/BPFormulaOption.m
Cakebrew/Models/BPFormula.h
Cakebrew/Models/BPFormula.m
Cakebrew/Models/BPFormulaOption.h
Cakebrew/Controllers/BPFormulaPopoverViewController.h
Cakebrew/Controllers/BPFormulaOptionsWindowController.m
====
---- Cakebrew/Models/BPFormulaOption.m ----
21:- (instancetype)initWithCoder:(NSCoder *)aDecoder
25:		_name = [aDecoder decodeObjectOfClass:[NSString class] forKey:kBPFormulaOptionNameKey];
26:		_explanation = [aDecoder decodeObjectOfClass:[NSString class] forKey:kBPFormulaOptionExplanationKey];
31:- (void)encodeWithCoder:(NSCoder *)aCoder
33:	[aCoder encodeObject:self.name forKey:kBPFormulaOptionNameKey];
34:	[aCoder encodeObject:self.explanation forKey:kBPFormulaOptionExplanationKey];
---- Cakebrew/Models/BPFormula.m ----
94:- (void)encodeWithCoder:(NSCoder *)aCoder
96:	if (self.name)				[aCoder encodeObject:self.name				forKey:kBP_ENCODE_FORMULA_NAME];
97:	if (self.version)			[aCoder encodeObject:self.version			forKey:kBP_ENCODE_FORMULA_IVER];
98:	if (self.latestVersion)		[aCoder encodeObject:self.latestVersion		forKey:kBP_ENCODE_FORMULA_LVER];
99:	if (self.installPath)		[aCoder encodeObject:self.installPath		forKey:kBP_ENCODE_FORMULA_PATH];
100:	if (self.website)			[aCoder encodeObject:self.website			forKey:kBP_ENCODE_FORMULA_WURL];
101:	if (self.dependencies)		[aCoder encodeObject:self.dependencies		forKey:kBP_ENCODE_FORMULA_DEPS];
102:	if (self.conflicts)			[aCoder encodeObject:self.conflicts			forKey:kBP_ENCODE_FORMULA_CNFL];
103:	if (self.shortDescription)	[aCoder encodeObject:self.shortDescription	forKey:kBP_ENCODE_FORMULA_SDSC];
104:	if (self.information)		[aCoder encodeObject:self.information		forKey:kBP_ENCODE_FORMULA_INFO];
105:	if (self.options)			[aCoder encodeObject:self.options			forKey:kBP_ENCODE_FORMULA_OPTN];
106:	[aCoder encodeObject:@([self isInstalled]) forKey:kBP_ENCODE_FORMULA_INST];
109:- (instancetype)initWithCoder:(NSCoder *)aDecoder
114:		self.name				= [aDecoder decodeObjectOfClass:[NSString class] forKey:kBP_ENCODE_FORMULA_NAME];
115:		self.version			= [aDecoder decodeObjectOfClass:[NSString class] forKey:kBP_ENCODE_FORMULA_IVER];
116:		self.latestVersion		= [aDecoder decodeObjectOfClass:[NSString class] forKey:kBP_ENCODE_FORMULA_LVER];
117:		self.installPath		= [aDecoder decodeObjectOfClass:[NSString class] forKey:kBP_ENCODE_FORMULA_PATH];
118:		self.website			= [aDecoder decodeObjectOfClass:[NSURL class] forKey:kBP_ENCODE_FORMULA_WURL];
119:		self.dependencies		= [aDecoder decodeObjectOfClass:[NSString class] forKey:kBP_ENCODE_FORMULA_DEPS];
120:		self.conflicts			= [aDecoder decodeObjectOfClass:[NSString class] forKey:kBP_ENCODE_FORMULA_CNFL];
121:		self.shortDescription	= [aDecoder decodeObjectOfClass:[NSString class] forKey:kBP_ENCODE_FORMULA_CNFL];
122:		self.information		= [aDecoder decodeObjectOfClass:[NSString class] forKey:kBP_ENCODE_FORMULA_INFO];
125:		self.options			= [aDecoder decodeObjectOfClasses:optionsClasses forKey:kBP_ENCODE_FORMULA_OPTN];
```

> TOOL

tool_use Read
id: toolu_01FgsXtQuARAQcJiZ1umHFXX
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/Models/BPFormula.m",
  "offset": 109,
  "limit": 25
}
```

> TOOL

tool_result
id: toolu_01FgsXtQuARAQcJiZ1umHFXX
```
109	- (instancetype)initWithCoder:(NSCoder *)aDecoder
110	{
111		self = [super init];
112		if (self)
113		{
114			self.name				= [aDecoder decodeObjectOfClass:[NSString class] forKey:kBP_ENCODE_FORMULA_NAME];
115			self.version			= [aDecoder decodeObjectOfClass:[NSString class] forKey:kBP_ENCODE_FORMULA_IVER];
116			self.latestVersion		= [aDecoder decodeObjectOfClass:[NSString class] forKey:kBP_ENCODE_FORMULA_LVER];
117			self.installPath		= [aDecoder decodeObjectOfClass:[NSString class] forKey:kBP_ENCODE_FORMULA_PATH];
118			self.website			= [aDecoder decodeObjectOfClass:[NSURL class] forKey:kBP_ENCODE_FORMULA_WURL];
119			self.dependencies		= [aDecoder decodeObjectOfClass:[NSString class] forKey:kBP_ENCODE_FORMULA_DEPS];
120			self.conflicts			= [aDecoder decodeObjectOfClass:[NSString class] forKey:kBP_ENCODE_FORMULA_CNFL];
121			self.shortDescription	= [aDecoder decodeObjectOfClass:[NSString class] forKey:kBP_ENCODE_FORMULA_CNFL];
122			self.information		= [aDecoder decodeObjectOfClass:[NSString class] forKey:kBP_ENCODE_FORMULA_INFO];
123	
124			NSSet *optionsClasses = [NSSet setWithArray:@[[NSArray class], [BPFormulaOption class]]];
125			self.options			= [aDecoder decodeObjectOfClasses:optionsClasses forKey:kBP_ENCODE_FORMULA_OPTN];
126			[self commonInit];
127		}
128		return self;
129	}
130	
131	- (void)commonInit
132	{
133		[self addObserver:self
```

> AGENT

Confirmed. Line 124 of `BPFormula.m` already correctly uses `[NSArray class]` for its inner `options`, but the top-level decode in `BPHomebrewManager.m:156` only allows `NSMutableArray` — so the immutable `NSArray` container that wraps the formulae gets rejected. Both Copilot findings are valid. Applying both fixes:

> TOOL

tool_use Edit
id: toolu_01Xt9CLKBzLZQ8Tdi3NzAXrC
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/BPHomebrewManager.m",
  "old_string": "\t\t\t\tNSSet *classes = [NSSet setWithArray:@[[NSDictionary class], [NSMutableArray class], [BPFormula class], [NSString class], [NSURL class], [NSNumber class], [BPFormulaOption class]]];",
  "new_string": "\t\t\t\tNSSet *classes = [NSSet setWithArray:@[[NSDictionary class], [NSArray class], [NSMutableArray class], [BPFormula class], [NSString class], [NSURL class], [NSNumber class], [BPFormulaOption class]]];"
}
```

> TOOL

tool_result
id: toolu_01Xt9CLKBzLZQ8Tdi3NzAXrC
```
The file /home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/BPHomebrewManager.m has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01YXjxdB2gtGwoTy21cx6BXU
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/Controllers/BPSideBarController.m",
  "old_string": "\tself = [super init];\n\tif (self) {\n\t\t_mutableChildren = [NSMutableArray array];\n\t}\n\treturn self;",
  "new_string": "\tself = [super init];\n\tif (self) {\n\t\t_mutableChildren = [NSMutableArray array];\n\t\t_badgeValue = @(-1); // Hidden by default until a real count is assigned\n\t}\n\treturn self;"
}
```

> TOOL

tool_result
id: toolu_01YXjxdB2gtGwoTy21cx6BXU
```
The file /home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/Controllers/BPSideBarController.m has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Both fixes applied. Rebuilding to confirm.

> TOOL

tool_use Bash
id: toolu_01QDu2tuhWL6mdb3NU9MxycX
```json
{
  "command": "xcodebuild -workspace Cakebrew.xcworkspace -scheme Cakebrew -configuration Debug -destination 'platform=macOS' build 2>&1 | grep -E \"error:|BUILD SUCCEEDED|BUILD FAILED\" | tail -10",
  "description": "Rebuild after the two fixes",
  "timeout": 420000
}
```

> TOOL

tool_result
id: toolu_01QDu2tuhWL6mdb3NU9MxycX
```
** BUILD SUCCEEDED ** [3.431 sec]
```

> AGENT

Build is clean. Committing and pushing.

> TOOL

tool_use Bash
id: toolu_01Dkqwvsb6r8rzD1wAXJ3mkW
```json
{
  "command": "git add Cakebrew/BPHomebrewManager.m Cakebrew/Controllers/BPSideBarController.m && git commit -m \"$(cat <<'EOF'\nAddress PR re-review: fix cache decode and default badge state\n\n- Add NSArray to the secure-unarchiving allowed classes in\n  storeAllFormulaeCaches's loader. The cached value is an immutable\n  NSArray<BPFormula *>; allowing only NSMutableArray (a subclass)\n  rejected the container, so the cache silently never loaded.\n- Default BPSidebarItem.badgeValue to @(-1) so sidebar items are\n  badge-hidden until refreshSidebarBadges assigns a real count,\n  instead of momentarily showing \"0\".\n\nCo-Authored-By: Claude Opus 4.7 (1M context) <<REDACTED_EMAIL>>\nEOF\n)\" && git push 2>&1 | tail -3",
  "description": "Commit and push the re-review fixes"
}
```

> TOOL

tool_result
id: toolu_01Dkqwvsb6r8rzD1wAXJ3mkW
```
[modernize-macos26 69622cd] Address PR re-review: fix cache decode and default badge state
 2 files changed, 2 insertions(+), 1 deletion(-)
To https://github.com/scottdensmore/Cakebrew.git
   5e89ec8..69622cd  modernize-macos26 -> modernize-macos26
```

> AGENT

Now I'll reply to the two new threads and resolve them.

> TOOL

tool_use Bash
id: toolu_01LgzCQ5Zst1Gd1ddGDMZU2Z
```json
{
  "command": "R=\"repos/scottdensmore/Cakebrew/pulls/1/comments\"\ngh api $R -F in_reply_to=3300709930 -f body=\"Good catch — fixed in 69622cd. Added \\`[NSArray class]\\` to the allowed-classes set. The cached value is an immutable \\`NSArray<BPFormula *>\\`, and \\`NSMutableArray\\` (a subclass) doesn't permit it, so secure decoding was failing and the cache never loaded. (Note BPFormula's own initWithCoder already allowed NSArray for its options.)\" --jq .id\ngh api $R -F in_reply_to=3300709944 -f body=\"Fixed in 69622cd — \\`BPSidebarItem.badgeValue\\` now defaults to \\`@(-1)\\` in \\`init\\`, so items are badge-hidden until \\`refreshSidebarBadges\\` assigns a real count, rather than showing \\\"0\\\".\" --jq .id\necho \"==== resolving threads ====\"\nM='mutation($id:ID!){resolveReviewThread(input:{threadId:$id}){thread{isResolved}}}'\nfor T in PRRT_kwDOA4x9PM6EqMD5 PRRT_kwDOA4x9PM6EqMEF; do echo -n \"$T -> \"; gh api graphql -f query=\"$M\" -f id=\"$T\" --jq '.data.resolveReviewThread.thread.isResolved'; done",
  "description": "Reply to and resolve the two new review threads"
}
```

> TOOL

tool_result
id: toolu_01LgzCQ5Zst1Gd1ddGDMZU2Z
```
3300840249
3300840309
==== resolving threads ====
PRRT_kwDOA4x9PM6EqMD5 -> true
PRRT_kwDOA4x9PM6EqMEF -> true
```

> AGENT

Both new findings are addressed, pushed as `69622cd`, build passes, and both threads are resolved.

## Copilot re-review results

It flagged **2 new issues** — both legit, both fixed:

1. **Cache decode bug** (`BPHomebrewManager.m:156`) — the real find. The secure-unarchiving allow-list had `NSMutableArray` but not `NSArray`. The cached value is an immutable `NSArray<BPFormula*>`, and a subclass entry doesn't permit the superclass, so decoding silently failed and the formula cache **never loaded** (the app would re-fetch from brew every launch). Added `[NSArray class]`. This was a latent bug from the branch's earlier switch to secure coding — not the sidebar work.
2. **Badge default state** (`BPSideBarController.m`) — in my sidebar code, a nil `badgeValue` would render as "0" instead of hidden. Now defaults to `@(-1)` in `BPSidebarItem init`.

It also auto-suppressed one low-confidence note (no thread created), so nothing to action there.

## PR status
- **9 of 10 threads resolved.** The only open one is still `DEVELOPMENT_TEAM`, intentionally kept (your signing team) and awaiting your call.
- Build: **SUCCEEDED**. PR is unmerged.

Want me to **request one more Copilot pass** to confirm it's clean, **resolve the `DEVELOPMENT_TEAM` thread**, or are you ready to **squash-merge**?

> DEVELOPER

yes request and then we can address and sqaush and merge

> AGENT

Requesting another Copilot pass, then I'll watch for it to land.

> TOOL

tool_use Bash
id: toolu_01SXTc4boFDZEbA877qUnKch
```json
{
  "command": "gh api graphql -f query='\nmutation {\n  requestReviews(input: {pullRequestId: \"PR_kwDOA4x9PM7fMhSD\", botIds: [\"BOT_kgDOCnlnWA\"], union: true}) {\n    pullRequest { reviewRequests(first: 10) { nodes { requestedReviewer { __typename ... on Bot { login } } } } }\n  }\n}' --jq '.data.requestReviews.pullRequest.reviewRequests.nodes[].requestedReviewer.login'",
  "description": "Request a third Copilot review"
}
```

> TOOL

tool_result
id: toolu_01SXTc4boFDZEbA877qUnKch
```
copilot-pull-request-reviewer
```

> TOOL

tool_use Bash
id: toolu_01F4xhvmQAkncJYkjYwe6sAn
```json
{
  "command": "until [ \"$(gh pr view 1 --repo scottdensmore/Cakebrew --json reviews --jq '[.reviews[] | select(.author.login==\"copilot-pull-request-reviewer\")] | length')\" -ge 3 ]; do sleep 15; done; echo \"Copilot third review has landed\"",
  "description": "Poll until Copilot's third review posts",
  "run_in_background": true
}
```

> TOOL

tool_result
id: toolu_01F4xhvmQAkncJYkjYwe6sAn
```
Command running in background with ID: b7gqy44fr. Output is being written to: /private/tmp/claude-501/-Users-scottdensmore-Developer-scottdensmore-cakebrew/86f7230f-16a2-4201-9dae-105c1789c2c6/tasks/b7gqy44fr.output. You will be notified when it completes. To check interim output, use Read on that file path.
```

> AGENT

Re-review requested and I'm watching for it in the background. Once it lands I'll:
1. Pull any new findings and assess them,
2. Fix + reply/resolve anything actionable (and report back if something needs your judgment),
3. Then squash-merge the PR into `master`.

I'll report when the review posts. If it comes back clean, I'll go straight to the squash-merge.

> AGENT

The third review landed. Let me pull its findings.

> TOOL

tool_use Bash
id: toolu_01SM2wFsBX886tEsAttgSY6V
```json
{
  "command": "echo \"==== latest Copilot review body ====\"; gh pr view 1 --repo scottdensmore/Cakebrew --json reviews --jq '[.reviews[] | select(.author.login==\"copilot-pull-request-reviewer\")] | last | {at:.submittedAt, body:.body}'; echo; echo \"==== unresolved review threads ====\"; gh api graphql -f query='\nquery {\n  repository(owner: \"scottdensmore\", name: \"Cakebrew\") {\n    pullRequest(number: 1) {\n      reviewThreads(first: 50) {\n        nodes { id isResolved isOutdated\n          comments(first: 10) { nodes { databaseId author { login } path originalLine createdAt body } } }\n      }\n    }\n  }\n}' --jq '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved==false) | {threadId:.id, comments:[.comments.nodes[]|{id:.databaseId, user:.author.login, path:.path, line:.originalLine, created:.created, body:.body}]}'",
  "description": "Fetch latest Copilot review and unresolved threads"
}
```

> TOOL

tool_result
id: toolu_01SM2wFsBX886tEsAttgSY6V
```
==== latest Copilot review body ====
{"at":"2026-05-26T02:44:54Z","body":"## Pull request overview\n\nCopilot reviewed 56 out of 215 changed files in this pull request and generated 4 comments.\n\n\u003cdetails\u003e\n\u003csummary\u003eFiles not reviewed (1)\u003c/summary\u003e\n\n* **Cakebrew.xcworkspace/contents.xcworkspacedata**: Language not supported\n\u003c/details\u003e\n\n\n\u003cdetails\u003e\n\u003csummary\u003eComments suppressed due to low confidence (1)\u003c/summary\u003e\n\n**Cakebrew.xcodeproj/project.pbxproj:31**\n* `dsa_pub.pem` is still being bundled as an app resource even though Sparkle has been removed. This file appears Sparkle-specific (DSA public key) and keeping it around is confusing/dead weight; consider removing it from the project/resources as part of fully dropping Sparkle (and removing any remaining Sparkle-related Info.plist keys if still present).\n```\n\t\t1584884A1F0708F000BD2CD9 /* brewinfo_nmap.txt in Resources */ = {isa = PBXBuildFile; fileRef = 158488491F0708F000BD2CD9 /* brewinfo_nmap.txt */; };\n\t\t1594D13C1B8A6D1A00F764FA /* QuartzCore.framework in Frameworks */ = {isa = PBXBuildFile; fileRef = 15D2CFAC18F202D000B6D9F1 /* QuartzCore.framework */; };\n\t\t15A00B411B8406FB00528486 /* Credits.rtf in Resources */ = {isa = PBXBuildFile; fileRef = 15A00B401B8406FB00528486 /* Credits.rtf */; };\n\t\t15A89D3925F2F467003D33F5 /* NSLayoutConstraint+Shims.m in Sources */ = {isa = PBXBuildFile; fileRef = 15A89D3825F2F467003D33F5 /* NSLayoutConstraint+Shims.m */; };\n\t\t15B23A2C18F5003600714212 /* dsa_pub.pem in Resources */ = {isa = PBXBuildFile; fileRef = 15B23A2B18F5003600714212 /* dsa_pub.pem */; };\n\t\t15BBA18E1BD031C9002C0127 /* BPBackgroundView.m in Sources */ = {isa = PBXBuildFile; fileRef = 15BBA18D1BD031C9002C0127 /* BPBackgroundView.m */; };\n\t\t15C34CBF19512DE100B92E36 /* BPAutoScrollTextView.m in Sources */ = {isa = PBXBuildFile; fileRef = […]

> AGENT

The third pass surfaced **4 new comments** (all in the pre-existing modernization code, not the sidebar) plus a suppressed note about a leftover Sparkle `dsa_pub.pem`. Let me read the relevant code to assess each properly before fixing.

> TOOL

tool_use Read
id: toolu_01CCT9ZYsjFJ2MJcPjTk4y2E
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/BPHomebrewManager.m",
  "offset": 120,
  "limit": 20
}
```

> TOOL

tool_result
id: toolu_01CCT9ZYsjFJ2MJcPjTk4y2E
```
120	
121		dispatch_async(dispatch_get_main_queue(), ^{
122			[self.delegate homebrewManager:self didUpdateSearchResults:matches];
123		});
124	}
125	
126	/**
127	 Returns `YES` if cache exists, was created less than 24 hours ago and was loaded successfully. Otherwise returns `NO`.
128	 */
129	- (BOOL)loadAllFormulaeCaches
130	{
131		NSURL *cachesFolder = [BPAppDelegate urlForApplicationCachesFolder];
132		NSURL *allFormulaeFile = [cachesFolder URLByAppendingPathComponent:@"allFormulae.cache.bin"];
133		BOOL shouldLoadCache = NO;
134		
135		if ([[NSUserDefaults standardUserDefaults] objectForKey:kBPCacheLastUpdateKey])
136		{
137			NSDate *storageDate = [NSDate dateWithTimeIntervalSince1970:[[NSUserDefaults standardUserDefaults]
138																		 integerForKey:kBPCacheLastUpdateKey]];
139			
```

> TOOL

tool_use Bash
id: toolu_01XEpP4CjFxzq43RbyKhqxic
```json
{
  "command": "echo \"==== master storeAllFormulaeCaches storageDate block ====\"; git show master:Cakebrew/BPHomebrewManager.m 2>/dev/null | grep -n \"storageDate\\|kBPCacheLastUpdateKey\\|unarchiveObjectWithData\\|NSKeyedUnarchiver\\|requiringSecureCoding\" | head -30",
  "description": "Check master's cache timestamp and archiving logic"
}
```

> TOOL

tool_result
id: toolu_01XEpP4CjFxzq43RbyKhqxic
```
==== master storeAllFormulaeCaches storageDate block ====
26:NSString *const kBPCacheLastUpdateKey = @"BPCacheLastUpdateKey";
134:	if ([[NSUserDefaults standardUserDefaults] objectForKey:kBPCacheLastUpdateKey])
136:		NSDate *storageDate = [NSDate dateWithTimeIntervalSince1970:[[NSUserDefaults standardUserDefaults]
137:																	 integerForKey:kBPCacheLastUpdateKey]];
139:		if ([[NSDate date] timeIntervalSinceDate:storageDate] <= 3600*24)
156:				cacheDict = [NSKeyedUnarchiver unarchivedObjectOfClasses:classes fromData:data error:&error];
161:				cacheDict = [NSKeyedUnarchiver unarchiveObjectWithFile:allFormulaeFile.relativePath];
170:		[[NSUserDefaults standardUserDefaults] removeObjectForKey:kBPCacheLastUpdateKey];
184:			NSDate *storageDate = [NSDate date];
186:			if ([[NSUserDefaults standardUserDefaults] objectForKey:kBPCacheLastUpdateKey])
188:				storageDate = [NSDate dateWithTimeIntervalSince1970:[[NSUserDefaults standardUserDefaults]
189:																	 integerForKey:kBPCacheLastUpdateKey]];
198:												  requiringSecureCoding:YES
218:			[[NSUserDefaults standardUserDefaults] setInteger:[storageDate timeIntervalSince1970]
219:													   forKey:kBPCacheLastUpdateKey];
```

> TOOL

tool_result
id: toolu_01XtsYN6ZX5Af5iZtUeYwFax
```
30:@interface BPAppDelegate () <UNUserNotificationCenterDelegate>
60:	UNUserNotificationCenter *center = [UNUserNotificationCenter currentNotificationCenter];
77:	[self cleanupTaskAlerts];
92:- (void)cleanupTaskAlerts
94:	[[UNUserNotificationCenter currentNotificationCenter] removeAllDeliveredNotifications];
157:- (void)requestUserAttentionWithMessageTitle:(NSString*)title andDescription:(NSString*)desc
171:	UNTimeIntervalNotificationTrigger *trigger = [UNTimeIntervalNotificationTrigger triggerWithTimeInterval:0.1 repeats:NO];
174:	UNNotificationRequest *request = [UNNotificationRequest requestWithIdentifier:identifier content:content trigger:trigger];
176:	[[UNUserNotificationCenter currentNotificationCenter] addNotificationRequest:request withCompletionHandler:^(NSError * _Nullable error) {
198:- (void)userNotificationCenter:(UNUserNotificationCenter *)center 
202:	[self cleanupTaskAlerts];
206:- (void)userNotificationCenter:(UNUserNotificationCenter *)center
```

> TOOL

tool_use Bash
id: toolu_01XtsYN6ZX5Af5iZtUeYwFax
```json
{
  "command": "grep -n \"cleanupTaskAlerts\\|removeAllDelivered\\|removeAllPending\\|UNTimeIntervalNotificationTrigger\\|UNNotificationRequest\\|requestUserAttentionWithMessageTitle\\|addNotificationRequest\\|triggerWithTimeInterval\\|UNUserNotificationCenter\" Cakebrew/BPAppDelegate.m",
  "description": "Locate notification scheduling and cleanup in BPAppDelegate"
}
```

> AGENT

Key finding: comment **#2 (the `storageDate` timestamp logic) is identical on `master`** — it predates this PR and isn't part of the modernization, so I'll keep it out of scope rather than change long-standing cache behavior in a migration PR. The other three (#1 dead 10.13 fallback, #3 nil-data guard, #4 pending notifications) are all in code this branch introduced and are worth fixing. Let me read the exact regions.

> TOOL

tool_use Read
id: toolu_01RNnvNvMmv2Y4VpwZ9N7NkF
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/BPHomebrewManager.m",
  "offset": 153,
  "limit": 18
}
```

> TOOL

tool_result
id: toolu_01RNnvNvMmv2Y4VpwZ9N7NkF
```
153				NSError *error = nil;
154	
155				if (@available(macOS 10.13, *)) {
156					NSSet *classes = [NSSet setWithArray:@[[NSDictionary class], [NSArray class], [NSMutableArray class], [BPFormula class], [NSString class], [NSURL class], [NSNumber class], [BPFormulaOption class]]];
157					cacheDict = [NSKeyedUnarchiver unarchivedObjectOfClasses:classes fromData:data error:&error];
158					if (error) {
159						NSLog(@"Failed decoding data: %@", [error localizedDescription]);
160					}
161				} else {
162					// Fallback for older macOS versions
163					NSError *fallbackError = nil;
164					cacheDict = [NSKeyedUnarchiver unarchivedObjectOfClass:[NSDictionary class] fromData:data error:&fallbackError];
165					if (fallbackError) {
166						NSLog(@"Failed decoding data: %@", [fallbackError localizedDescription]);
167					}
168				}
169				self.allFormulae = [cacheDict objectForKey:kBPCacheDataKey];
170			}
```

> TOOL

tool_use Read
id: toolu_01Mvf57G2zFNLfEMxuodRe1s
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/BPAppDelegate.m",
  "offset": 88,
  "limit": 12
}
```

> TOOL

tool_result
id: toolu_01Mvf57G2zFNLfEMxuodRe1s
```
88	- (BOOL)applicationShouldTerminateAfterLastWindowClosed:(NSApplication *)sender {
89		return YES;
90	}
91	
92	- (void)cleanupTaskAlerts
93	{
94		[[UNUserNotificationCenter currentNotificationCenter] removeAllDeliveredNotifications];
95		[[[NSApplication sharedApplication] dockTile] setBadgeLabel:nil];
96	}
97	
98	+ (NSURL*)urlForApplicationSupportFolder
99	{
```

> AGENT

Now applying the three fixes — collapse the bogus 10.13 fallback to a single decode path, guard against nil archive data, and also clear pending notifications.

> TOOL

tool_use Edit
id: toolu_01VSJDiRt2pfR9c3k4ynxssq
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/BPHomebrewManager.m",
  "old_string": "\t\t\tNSError *error = nil;\n\n\t\t\t\tif (@available(macOS 10.13, *)) {\n\t\t\t\t\tNSSet *classes = [NSSet setWithArray:@[[NSDictionary class], [NSArray class], [NSMutableArray class], [BPFormula class], [NSString class], [NSURL class], [NSNumber class], [BPFormulaOption class]]];\n\t\t\t\t\tcacheDict = [NSKeyedUnarchiver unarchivedObjectOfClasses:classes fromData:data error:&error];\n\t\t\t\t\tif (error) {\n\t\t\t\t\t\tNSLog(@\"Failed decoding data: %@\", [error localizedDescription]);\n\t\t\t\t\t}\n\t\t\t\t} else {\n\t\t\t\t\t// Fallback for older macOS versions\n\t\t\t\t\tNSError *fallbackError = nil;\n\t\t\t\t\tcacheDict = [NSKeyedUnarchiver unarchivedObjectOfClass:[NSDictionary class] fromData:data error:&fallbackError];\n\t\t\t\t\tif (fallbackError) {\n\t\t\t\t\t\tNSLog(@\"Failed decoding data: %@\", [fallbackError localizedDescription]);\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t\tself.allFormulae = [cacheDict objectForKey:kBPCacheDataKey];",
  "new_string": "\t\t\tNSError *error = nil;\n\n\t\t\t\tNSSet *classes = [NSSet setWithArray:@[[NSDictionary class], [NSArray class], [NSMutableArray class], [BPFormula class], [NSString class], [NSURL class], [NSNumber class], [BPFormulaOption class]]];\n\t\t\t\tcacheDict = [NSKeyedUnarchiver unarchivedObjectOfClasses:classes fromData:data error:&error];\n\t\t\t\tif (error) {\n\t\t\t\t\tNSLog(@\"Failed decoding data: %@\", [error localizedDescription]);\n\t\t\t\t}\n\t\t\t\tself.allFormulae = [cacheDict objectForKey:kBPCacheDataKey];"
}
```

> TOOL

tool_result ERROR
id: toolu_01VSJDiRt2pfR9c3k4ynxssq
```
<tool_use_error>String to replace not found in file.
String: 			NSError *error = nil;

				if (@available(macOS 10.13, *)) {
					NSSet *classes = [NSSet setWithArray:@[[NSDictionary class], [NSArray class], [NSMutableArray class], [BPFormula class], [NSString class], [NSURL class], [NSNumber class], [BPFormulaOption class]]];
					cacheDict = [NSKeyedUnarchiver unarchivedObjectOfClasses:classes fromData:data error:&error];
					if (error) {
						NSLog(@"Failed decoding data: %@", [error localizedDescription]);
					}
				} else {
					// Fallback for older macOS versions
					NSError *fallbackError = nil;
					cacheDict = [NSKeyedUnarchiver unarchivedObjectOfClass:[NSDictionary class] fromData:data error:&fallbackError];
					if (fallbackError) {
						NSLog(@"Failed decoding data: %@", [fallbackError localizedDescription]);
					}
				}
				self.allFormulae = [cacheDict objectForKey:kBPCacheDataKey];</tool_use_error>
```

> TOOL

tool_use Edit
id: toolu_01GQAdJy5rTnNdRXbx6XgQjX
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/BPHomebrewManager.m",
  "old_string": "\t\t\tif (error) {\n\t\t\t\tNSLog(@\"Failed encoding data: %@\", [error localizedDescription]);\n\t\t\t}\n\t\t\t\n\t\t\tif ([[NSFileManager defaultManager] fileExistsAtPath:allFormulaeFile.relativePath])",
  "new_string": "\t\t\tif (error || !cacheData) {\n\t\t\t\tNSLog(@\"Failed encoding data: %@\", [error localizedDescription]);\n\t\t\t\treturn;\n\t\t\t}\n\n\t\t\tif ([[NSFileManager defaultManager] fileExistsAtPath:allFormulaeFile.relativePath])"
}
```

> TOOL

tool_result
id: toolu_01GQAdJy5rTnNdRXbx6XgQjX
```
The file /home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/BPHomebrewManager.m has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01UHHBJCUKXZhDZYnnyWR7X8
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/BPAppDelegate.m",
  "old_string": "- (void)cleanupTaskAlerts\n{\n\t[[UNUserNotificationCenter currentNotificationCenter] removeAllDeliveredNotifications];\n\t[[[NSApplication sharedApplication] dockTile] setBadgeLabel:nil];\n}",
  "new_string": "- (void)cleanupTaskAlerts\n{\n\tUNUserNotificationCenter *center = [UNUserNotificationCenter currentNotificationCenter];\n\t[center removeAllPendingNotificationRequests];\n\t[center removeAllDeliveredNotifications];\n\t[[[NSApplication sharedApplication] dockTile] setBadgeLabel:nil];\n}"
}
```

> TOOL

tool_result
id: toolu_01UHHBJCUKXZhDZYnnyWR7X8
```
The file /home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/BPAppDelegate.m has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

The second and third edits applied; the first failed on whitespace. Let me inspect the exact bytes of that block.

> TOOL

tool_use Bash
id: toolu_011UDQ4dj7q1vdXmp9WnNqPX
```json
{
  "command": "sed -n '153,169p' Cakebrew/BPHomebrewManager.m | cat -A | head -20",
  "description": "Reveal exact whitespace/tabs in the decode block"
}
```

> TOOL

tool_result
id: toolu_011UDQ4dj7q1vdXmp9WnNqPX
```
cat: illegal option -- A
usage: cat [-belnstuv] [file ...]
```

> TOOL

tool_use Bash
id: toolu_018SmFnpB38qKHXWMmxpBHKj
```json
{
  "command": "sed -n '153,169p' Cakebrew/BPHomebrewManager.m | cat -t -e",
  "description": "Show tabs and line ends in the decode block"
}
```

> TOOL

tool_result
id: toolu_018SmFnpB38qKHXWMmxpBHKj
```
^I^I^INSError *error = nil;$
$
^I^I^Iif (@available(macOS 10.13, *)) {$
^I^I^I^INSSet *classes = [NSSet setWithArray:@[[NSDictionary class], [NSArray class], [NSMutableArray class], [BPFormula class], [NSString class], [NSURL class], [NSNumber class], [BPFormulaOption class]]];$
^I^I^I^IcacheDict = [NSKeyedUnarchiver unarchivedObjectOfClasses:classes fromData:data error:&error];$
^I^I^I^Iif (error) {$
^I^I^I^I^INSLog(@"Failed decoding data: %@", [error localizedDescription]);$
^I^I^I^I}$
^I^I^I} else {$
^I^I^I^I// Fallback for older macOS versions$
^I^I^I^INSError *fallbackError = nil;$
^I^I^I^IcacheDict = [NSKeyedUnarchiver unarchivedObjectOfClass:[NSDictionary class] fromData:data error:&fallbackError];$
^I^I^I^Iif (fallbackError) {$
^I^I^I^I^INSLog(@"Failed decoding data: %@", [fallbackError localizedDescription]);$
^I^I^I^I}$
^I^I^I}$
^I^I^Iself.allFormulae = [cacheDict objectForKey:kBPCacheDataKey];$
```

> AGENT

Now I have the exact indentation (the `if (@available` is at 3 tabs, not 4). Correcting the edit:

> TOOL

tool_use Edit
id: toolu_01WZrPLuhU4kwjqT2W54zHAG
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/BPHomebrewManager.m",
  "old_string": "\t\t\tif (@available(macOS 10.13, *)) {\n\t\t\t\tNSSet *classes = [NSSet setWithArray:@[[NSDictionary class], [NSArray class], [NSMutableArray class], [BPFormula class], [NSString class], [NSURL class], [NSNumber class], [BPFormulaOption class]]];\n\t\t\t\tcacheDict = [NSKeyedUnarchiver unarchivedObjectOfClasses:classes fromData:data error:&error];\n\t\t\t\tif (error) {\n\t\t\t\t\tNSLog(@\"Failed decoding data: %@\", [error localizedDescription]);\n\t\t\t\t}\n\t\t\t} else {\n\t\t\t\t// Fallback for older macOS versions\n\t\t\t\tNSError *fallbackError = nil;\n\t\t\t\tcacheDict = [NSKeyedUnarchiver unarchivedObjectOfClass:[NSDictionary class] fromData:data error:&fallbackError];\n\t\t\t\tif (fallbackError) {\n\t\t\t\t\tNSLog(@\"Failed decoding data: %@\", [fallbackError localizedDescription]);\n\t\t\t\t}\n\t\t\t}\n\t\t\tself.allFormulae = [cacheDict objectForKey:kBPCacheDataKey];",
  "new_string": "\t\t\tNSSet *classes = [NSSet setWithArray:@[[NSDictionary class], [NSArray class], [NSMutableArray class], [BPFormula class], [NSString class], [NSURL class], [NSNumber class], [BPFormulaOption class]]];\n\t\t\tcacheDict = [NSKeyedUnarchiver unarchivedObjectOfClasses:classes fromData:data error:&error];\n\t\t\tif (error) {\n\t\t\t\tNSLog(@\"Failed decoding data: %@\", [error localizedDescription]);\n\t\t\t}\n\t\t\tself.allFormulae = [cacheDict objectForKey:kBPCacheDataKey];"
}
```

> TOOL

tool_result
id: toolu_01WZrPLuhU4kwjqT2W54zHAG
```
The file /home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/BPHomebrewManager.m has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

All three fixes are in. Rebuilding to confirm.

> TOOL

tool_use Bash
id: toolu_01NQz1TbxTecdZgQUnc6H58c
```json
{
  "command": "xcodebuild -workspace Cakebrew.xcworkspace -scheme Cakebrew -configuration Debug -destination 'platform=macOS' build 2>&1 | grep -E \"error:|warning:.*(BPHomebrewManager|BPAppDelegate)|BUILD SUCCEEDED|BUILD FAILED\" | tail -15",
  "description": "Rebuild after the three fixes",
  "timeout": 420000
}
```

> TOOL

tool_result
id: toolu_01NQz1TbxTecdZgQUnc6H58c
```
** BUILD SUCCEEDED ** [3.310 sec]
```

> AGENT

Build clean. Committing and pushing.

> TOOL

tool_use Bash
id: toolu_01X9ty33kUxSRyGdUJD5N6WA
```json
{
  "command": "git add Cakebrew/BPHomebrewManager.m Cakebrew/BPAppDelegate.m && git commit -m \"$(cat <<'EOF'\nAddress PR re-review: tidy cache decode and notification cleanup\n\n- Remove the bogus macOS 10.13 unarchive fallback. The else branch\n  used unarchivedObjectOfClass:, itself a 10.13+ API, and the\n  deployment target is macOS 26, so it was dead/misleading code.\n  Collapse to a single secure-decoding path.\n- Bail out of storeAllFormulaeCaches if secure archiving fails, so a\n  nil/empty payload isn't written and marked fresh.\n- Also clear pending notification requests in cleanupTaskAlerts, since\n  task alerts use a time-interval trigger and could otherwise fire\n  after cleanup.\n\nCo-Authored-By: Claude Opus 4.7 (1M context) <<REDACTED_EMAIL>>\nEOF\n)\" && git push 2>&1 | tail -3",
  "description": "Commit and push the third round of review fixes"
}
```

> TOOL

tool_result
id: toolu_01X9ty33kUxSRyGdUJD5N6WA
```
[modernize-macos26 8c440da] Address PR re-review: tidy cache decode and notification cleanup
 2 files changed, 10 insertions(+), 16 deletions(-)
To https://github.com/scottdensmore/Cakebrew.git
   69622cd..8c440da  modernize-macos26 -> modernize-macos26
```

> AGENT

Now I'll reply to the four threads — resolving the three I fixed, and explaining the one I'm intentionally leaving (the pre-existing timestamp behavior).

> TOOL

tool_use Bash
id: toolu_01SpojmMwvxfebFX8WBc5Ws3
```json
{
  "command": "R=\"repos/scottdensmore/Cakebrew/pulls/1/comments\"\ngh api $R -F in_reply_to=3300883374 -f body=\"Fixed in 8c440da — removed the bogus fallback. \\`unarchivedObjectOfClass:fromData:error:\\` is itself 10.13+, and the deployment target is macOS 26, so the else branch was dead/misleading. Collapsed to a single secure-decoding path.\" --jq .id\ngh api $R -F in_reply_to=3300883405 -f body=\"Fixed in 8c440da — \\`storeAllFormulaeCaches\\` now bails out (early return) if archiving returns an error or nil data, so an empty/corrupt payload isn't written and marked fresh.\" --jq .id\ngh api $R -F in_reply_to=3300883421 -f body=\"Fixed in 8c440da — \\`cleanupTaskAlerts\\` now also calls \\`removeAllPendingNotificationRequests\\` before removing delivered ones, so a pending time-interval alert can't fire after cleanup.\" --jq .id\ngh api $R -F in_reply_to=3300883398 -f body=\"Good observation, but this \\`storageDate\\` logic is unchanged from master (verified — identical pre-existing code) and isn't part of this modernization PR. To keep this PR scoped to the macOS 26 / dependency-removal work, I'm leaving it as-is; it's worth a separate follow-up rather than mixing a cache-freshness behavior change in here.\" --jq .id\necho \"==== resolving the three fixed threads ====\"\nM='mutation($id:ID!){resolveReviewThread(input:{threadId:$id}){thread{isResolved}}}'\nfor T in PRRT_kwDOA4x9PM6EqqqR PRRT_kwDOA4x9PM6Eqqqp PRRT_kwDOA4x9PM6Eqqq0; do echo -n \"$T -> \"; gh api graphql -f query=\"$M\" -f id=\"$T\" --jq '.data.resolveReviewThread.thread.isResolved'; done",
  "description": "Reply to all […]

> TOOL

tool_result
id: toolu_01SpojmMwvxfebFX8WBc5Ws3
```
3300915289
3300915339
3300915413
3300915472
==== resolving the three fixed threads ====
PRRT_kwDOA4x9PM6EqqqR -> true
PRRT_kwDOA4x9PM6Eqqqp -> true
PRRT_kwDOA4x9PM6Eqqq0 -> true
```

> AGENT

All actionable findings are fixed and resolved. Squash-merging the PR into `master` now.

> TOOL

tool_use Bash
id: toolu_01J8NRERPeC1cs11zJNQg34k
```json
{
  "command": "gh pr merge 1 --repo scottdensmore/Cakebrew --squash --subject \"Modernize for macOS 26: drop Sparkle & PXSourceList\" --body \"$(cat <<'EOF'\nRemoves the vendored Sparkle framework and the PXSourceList submodule and\nmigrates the sidebar to a native NSOutlineView source list, so the app\nbuilds and runs against the macOS 26 SDK.\n\n- Native NSOutlineView sidebar (BPSidebarItem / BPSidebarTableCellView /\n  BPSidebarBadgeView) replacing PXSourceList; data source, delegate, group\n  rows, and badge drawing reimplemented.\n- Remove Sparkle.framework and PXSourceList from the project, workspace, and\n  code; drop the now-dead \"Check for Updates…\" menu item.\n- Fix secure-coding cache decode (allow NSArray), collapse the dead 10.13\n  fallback, guard against nil archive data, and clear pending notifications\n  on cleanup.\n- Stable bundle identifiers; gitignore generated .genkit metadata.\nEOF\n)\" 2>&1 | tail -5; echo \"==== PR state ====\"; gh pr view 1 --repo scottdensmore/Cakebrew --json state,mergedAt,mergeCommit --jq '{state,mergedAt,mergeCommit:.mergeCommit.oid}'",
  "description": "Squash merge the PR into master"
}
```

> TOOL

tool_result
id: toolu_01J8NRERPeC1cs11zJNQg34k
```
==== PR state ====
{"mergeCommit":"f755a5c0f5ec993fa64b778242ed068da557f304","mergedAt":"2026-05-26T02:59:28Z","state":"MERGED"}
```

> AGENT

Merged. 🎉 PR #1 is squash-merged into `master` as commit `f755a5c`.

## Final summary

**Third Copilot pass — 4 comments, all handled** (pushed in `8c440da`, build verified):
| Finding | Action |
|---|---|
| Dead macOS 10.13 unarchive fallback (used a 10.13+ API anyway) | **Fixed** — collapsed to one secure-decode path |
| `storeAllFormulaeCaches` writes nil/empty data on archive failure | **Fixed** — early return on error/nil |
| `cleanupTaskAlerts` left pending (time-triggered) notifications | **Fixed** — also clears pending requests |
| `storageDate` timestamp never advances on write | **Declined** — verified identical on `master`, pre-existing and unrelated to this PR; replied suggesting a separate follow-up |

**Two threads intentionally left open**, each with an explanation on the PR:
- `DEVELOPMENT_TEAM` — your signing team, correct as-is.
- `storageDate` — pre-existing behavior, out of scope.

Over the three review rounds: **14 Copilot findings → 11 fixed, 3 declined with rationale.** Each round's fixes were rebuilt (all **BUILD SUCCEEDED**) before merge.

## Two notes
1. Your local checkout is still on `modernize-macos26`, and local `master` is now behind origin. Want me to fast-forward local `master` and (optionally) delete the merged feature branch?
2. Copilot also flagged (low-confidence, no thread) […]

> TOOL

tool_use mcp__ccd_session__spawn_task
id: toolu_01A1LaFpNo5sGfc9iXapkTNs
```json
{
  "title": "Remove leftover Sparkle dsa_pub.pem resource",
  "prompt": "Sparkle was fully removed from the Cakebrew app (the Sparkle.framework and its updater were deleted, and the \"Check for Updates…\" menu item was removed). However, the file Cakebrew/dsa_pub.pem — Sparkle's DSA public key used for verifying update signatures — is still bundled as an app resource and is now dead weight.\n\nPlease:\n1. Delete the Cakebrew/dsa_pub.pem file.\n2. Remove its references from Cakebrew.xcodeproj/project.pbxproj — there are two: a PBXBuildFile entry (id 15B23A2C18F5003600714212, \"dsa_pub.pem in Resources\") and a PBXFileReference (id 15B23A2B18F5003600714212), plus its entry in the Resources (PBXResourcesBuildPhase) files list and in whatever PBXGroup lists it.\n3. Check Cakebrew/Cakebrew-Info.plist (and any other Info.plist) for leftover Sparkle keys (SUFeedURL, SUPublicDSAKeyFile, SUEnableAutomaticChecks, SUScheduledCheckInterval, etc.) and remove them.\n4. Build with: xcodebuild -workspace Cakebrew.xcworkspace -scheme Cakebrew -configuration Debug -destination 'platform=macOS' build — confirm BUILD SUCCEEDED.\n\nFollow the repo's git workflow: do this on a branch, open a PR, and squash merge (do not commit to master directly).",
  "tldr": "Sparkle is gone but its DSA public key (dsa_pub.pem) is still bundled. This removes the file, its Xcode project references, and any leftover Sparkle Info.plist keys."
}
```

> TOOL

tool_result
id: toolu_01A1LaFpNo5sGfc9iXapkTNs
```
Noted (position 2). A chip is showing for the user — they can start it in a fresh worktree with one click, or dismiss it. Continue your current work.
```

> AGENT

The PR is merged and the follow-up for the leftover `dsa_pub.pem` is queued. Just let me know if you'd like me to sync your local `master` (and clean up the `modernize-macos26` branch), and you're all set.

> DEVELOPER

Is everything ready to create a pr and ready to merge? You create two background tasks that are now finished

> AGENT

Let me check what those two finished tasks produced — worktrees, branches, commits, and any open PRs.

> TOOL

tool_use Bash
id: toolu_01DfzfNLbdqHZDQ6ApUMMpnK
```json
{
  "command": "echo \"==== worktrees ====\"; git worktree list; echo \"==== local branches ====\"; git branch -vv; echo \"==== current status ====\"; git status -sb",
  "description": "Inspect worktrees, branches, and current status"
}
```

> TOOL

tool_result
id: toolu_01DfzfNLbdqHZDQ6ApUMMpnK
```
==== worktrees ====
/home/<USER>/Developer/scottdensmore/cakebrew 77f5ade [modernize-macos26]
==== local branches ====
  entire/0831032-e3b0c4 4aec067 Claude Code session updates
  entire/77f5ade-e3b0c4 f7cf76f Claude Code session updates
  entire/checkpoints/v1 08777ac Initialize metadata branch
  master                1053fe6 [origin/master: behind 1] Bump build to 594
* modernize-macos26     77f5ade [origin/modernize-macos26] Remove leftover Sparkle DSA key and updater plist keys (#2)
==== current status ====
## modernize-macos26...origin/modernize-macos26
 M Cakebrew/Credits.rtf
 M Cakebrew/pt.lproj/Credits.rtf
?? .claude/
?? .codex/
?? .entire/
?? .github/
```

> TOOL

tool_use Bash
id: toolu_01VaYcj56nyKKjKtPFqHpWb5
```json
{
  "command": "echo \"==== remote branches ====\"; git ls-remote --heads origin 2>/dev/null; echo \"==== open PRs ====\"; gh pr list --repo scottdensmore/Cakebrew --state open --json number,title,headRefName,mergeable,reviewDecision 2>/dev/null; echo \"==== all PRs (recent) ====\"; gh pr list --repo scottdensmore/Cakebrew --state all --limit 10 --json number,title,state,headRefName 2>/dev/null",
  "description": "Check remote branches and PR list"
}
```

> TOOL

tool_result
id: toolu_01VaYcj56nyKKjKtPFqHpWb5
```
==== remote branches ====
7d53bb64a5e2c5eeff8d871597a63a9eb45da42a	refs/heads/appcenter
60589d3f43fc000744b92b56647c8cb4bd2f6da5	refs/heads/dev
08777acecd07fa66c6874552af2327368f4ed6d2	refs/heads/entire/checkpoints/v1
9554b5b9e856bd9d8577908cf9c59dbda84db9f0	refs/heads/install-homebrew
f755a5c0f5ec993fa64b778242ed068da557f304	refs/heads/master
77f5ade1e1feb1553a52dd89618774c1daa062f2	refs/heads/modernize-macos26
0dbe9317877c7ce9b2ac7a047f6f323b003f6874	refs/heads/wip
==== open PRs ====
[]
==== all PRs (recent) ====
[{"headRefName":"remove-sparkle-dsa-key","number":2,"state":"MERGED","title":"Remove leftover Sparkle DSA key and updater plist keys"},{"headRefName":"modernize-macos26","number":1,"state":"MERGED","title":"Modernize for macOS 26: drop Sparkle & PXSourceList"}]
```

> AGENT

Interesting — there's more state here than expected. Let me map the full picture before answering.

> TOOL

tool_use Bash
id: toolu_013E5makiaGz8ZRMyoNMPh3x
```json
{
  "command": "echo \"==== graph (all branches) ====\"; git log --oneline --graph --all -18; echo; echo \"==== does origin/master contain current HEAD (77f5ade)? ====\"; git merge-base --is-ancestor 77f5ade origin/master && echo \"YES - HEAD is on master\" || echo \"NO - HEAD not yet on master\"; echo \"==== origin/master log ====\"; git log --oneline origin/master -6",
  "description": "Show commit graph and whether HEAD is merged to master"
}
```

> TOOL

tool_result
id: toolu_013E5makiaGz8ZRMyoNMPh3x
```
==== graph (all branches) ====
* f7cf76f Claude Code session updates
* 4aec067 Claude Code session updates
* 77f5ade Remove leftover Sparkle DSA key and updater plist keys (#2)
* 8c440da Address PR re-review: tidy cache decode and notification cleanup
* 69622cd Address PR re-review: fix cache decode and default badge state
* 5e89ec8 Address PR review: clean bundle ids, drop dead update menu, fix typo
* 952d98a Migrate sidebar from PXSourceList to native NSOutlineView
* 50117e5 Remove PXSourceList submodule
* 76c5ffd Remove Sparkle.framework and fix acknowledgements URL handling
| * 08777ac Initialize metadata branch
| * f755a5c Modernize for macOS 26: drop Sparkle & PXSourceList
|/  
* 1053fe6 Bump build to 594
* 56eac5c Revert fix for Sidebar
* db35975 Bump build to 593
* 351cddf Update credits file
* 128b80e Update sparkle framework
* 7f5c4b8 Fix deprecated API usages for 10.10
* 6ed3e41 Bump build to 592

==== does origin/master contain current HEAD (77f5ade)? ====
NO - HEAD not yet on master
==== origin/master log ====
f755a5c Modernize for macOS 26: drop Sparkle & PXSourceList
1053fe6 Bump build to 594
56eac5c Revert fix for Sidebar
db35975 Bump build to 593
351cddf Update credits file […]

> TOOL

tool_use Bash
id: toolu_01F9kyQfgjRJAHi3L534DugW
```json
{
  "command": "echo \"==== uncommitted Credits diff (stat) ====\"; git diff --stat; echo; echo \"==== Credits.rtf change content (PXSourceList lines) ====\"; git diff -- Cakebrew/Credits.rtf Cakebrew/pt.lproj/Credits.rtf | grep -iE \"^[-+].*(PXSourceList|Rozanski)\" | head; echo; echo \"==== still any PXSourceList left in Credits after change? ====\"; grep -l \"PXSourceList\" Cakebrew/Credits.rtf Cakebrew/pt.lproj/Credits.rtf 2>/dev/null || echo \"none remaining\"",
  "description": "Inspect the uncommitted Credits changes"
}
```

> TOOL

tool_result
id: toolu_01F9kyQfgjRJAHi3L534DugW
```
==== uncommitted Credits diff (stat) ====
 Cakebrew/Credits.rtf          | 8 --------
 Cakebrew/pt.lproj/Credits.rtf | 4 ----
 2 files changed, 12 deletions(-)

==== Credits.rtf change content (PXSourceList lines) ====
-\ls2\ilvl0\cf0 {\listtext	\uc0\u8226 	}{\field{\*\fldinst{HYPERLINK "https://github.com/brunophilipe/PXSourceList"}}{\fldrslt PXSourceList}} by Alex Rozanski\
-\ls2\ilvl1\cf0 {\listtext	\uc0\u8259 	}Copyright \'a9 2009-14, Alex Rozanski and other contributors.\
-\ls1\ilvl0\cf0 {\listtext	\'95	}{\field{\*\fldinst{HYPERLINK "https://github.com/Perspx/PXSourceList"}}{\fldrslt PXSourceList}} by Alex Rozanski\uc0\u8232 	Copyright \'a9 2009-14, Alex Rozanski and other contributors. All rights reserved.\

==== still any PXSourceList left in Credits after change? ====
none remaining
```

> AGENT

This is more tangled than expected. The key thing I see: **`origin/master` (f755a5c) and `modernize-macos26` (77f5ade) have diverged into parallel histories** — the squash-merge of PR #1 created a fresh commit on master, so the branch never caught up. I need to verify where PR #2 (the dsa removal) actually landed. Let me dig in.

> TOOL

tool_use Bash
id: toolu_01VJeMg2tqJVU3myahiaVPjA
```json
{
  "command": "echo \"==== PR #2 details ====\"; gh pr view 2 --repo scottdensmore/Cakebrew --json baseRefName,headRefName,state,mergedAt,mergeCommit --jq '{base:.baseRefName, head:.headRefName, state, mergedAt, mergeCommit:.mergeCommit.oid}'; echo; echo \"==== does origin/master still have dsa_pub.pem? ====\"; git ls-tree origin/master -- Cakebrew/dsa_pub.pem | grep -q . && echo \"PRESENT on master (dsa removal NOT in master)\" || echo \"absent from master\"; echo; echo \"==== what modernize-macos26 has that origin/master lacks ====\"; git diff origin/master..modernize-macos26 --stat | tail -30",
  "description": "Determine PR #2 base and divergence between master and modernize branch"
}
```

> TOOL

tool_result
id: toolu_01VJeMg2tqJVU3myahiaVPjA
```
==== PR #2 details ====
{"base":"modernize-macos26","head":"remove-sparkle-dsa-key","mergeCommit":"77f5ade1e1feb1553a52dd89618774c1daa062f2","mergedAt":"2026-05-26T03:21:45Z","state":"MERGED"}

==== does origin/master still have dsa_pub.pem? ====
PRESENT on master (dsa removal NOT in master)

==== what modernize-macos26 has that origin/master lacks ====
 Cakebrew.xcodeproj/project.pbxproj |  4 ----
 Cakebrew/Cakebrew-Info.plist       |  8 --------
 Cakebrew/dsa_pub.pem               | 20 --------------------
 3 files changed, 32 deletions(-)
```

> AGENT

I've now got the full picture, and **no — it's not ready yet.** The two finished tasks left things in a state that needs reconciling. Here's exactly what happened:

**1. The dsa-key removal (PR #2) merged into the wrong base.** That task opened PR #2 with base `modernize-macos26` instead of `master`, then squash-merged it there. So the dsa removal lives only on `modernize-macos26` — **`master` still has `dsa_pub.pem`** and the Sparkle Info.plist keys.

**2. The Credits cleanup is done but uncommitted** — the PXSourceList attribution is correctly removed from both `Credits.rtf` files (verified), but there's no commit, branch, or PR for it.

**3. `modernize-macos26` and `master` have diverged.** When PR #1 squash-merged, it created a fresh commit (`f755a5c`) on master. The old branch kept its original commits, so the two are now parallel histories. The *actual* content difference between them is small and clean though — exactly the remaining work:

```
Cakebrew.xcodeproj/project.pbxproj |  4 ----   (dsa)
Cakebrew/Cakebrew-Info.plist       |  8 ----   (dsa)
Cakebrew/dsa_pub.pem               | 20 ----   (dsa)
Cakebrew/Credits.rtf               |  8 ----   (credits, uncommitted)
Cakebrew/pt.lproj/Credits.rtf      |  4 ----   (credits, uncommitted)
```

So master is missing both the dsa removal and the credits cleanup. To land them cleanly I'd avoid re-using the diverged […]

> TOOL

tool_use AskUserQuestion
id: toolu_01G1mTMktdV8D6qszwgWUg7Q
```json
{
  "questions": [
    {
      "question": "How should I get the remaining changes (dsa removal + Credits cleanup) onto master?",
      "header": "Consolidate",
      "multiSelect": false,
      "options": [
        {
          "label": "Fresh branch off master (Recommended)",
          "description": "Create a new branch from origin/master containing only the net remaining diff (3 dsa files + 2 Credits files), open a PR against master, and squash merge. Clean single commit, no divergence/conflict risk."
        },
        {
          "label": "PR from modernize-macos26",
          "description": "Commit Credits there and PR modernize-macos26 -> master. Risky: GitHub will show the whole branch (all already-merged modernize commits) and may conflict, since master has the squashed equivalent."
        },
        {
          "label": "Just commit Credits, stop",
          "description": "Commit the Credits cleanup somewhere and stop; you'll decide how to handle the master reconciliation yourself."
        }
      ]
    }
  ]
}
```

> TOOL

tool_result
id: toolu_01G1mTMktdV8D6qszwgWUg7Q
```
Your questions have been answered: "How should I get the remaining changes (dsa removal + Credits cleanup) onto master?"="Fresh branch off master (Recommended)". You can now continue with these answers in mind.
```

> AGENT

Good call — the fresh-branch approach avoids all the divergence risk. Here's why it'll be clean: `master` (`f755a5c`) is the squash of `modernize-macos26` exactly at `8c440da`, which is the parent of the dsa commit `77f5ade`. So cherry-picking `77f5ade` onto master applies against an identical tree — zero conflicts.

Let me set it up: stash the Credits changes, branch off master, cherry-pick the dsa removal.

> TOOL

tool_use Bash
id: toolu_018BRWXxUWYPkKjQMu1J9wJG
```json
{
  "command": "git fetch origin --quiet && \\\ngit stash push -m \"credits cleanup\" -- Cakebrew/Credits.rtf Cakebrew/pt.lproj/Credits.rtf && \\\ngit checkout -b cleanup-modernization-leftovers origin/master && \\\necho \"==== clean checkout? ====\" && git status -sb | head -8",
  "description": "Stash credits, branch off origin/master"
}
```

> TOOL

tool_result
id: toolu_018BRWXxUWYPkKjQMu1J9wJG
```
Saved working directory and index state On modernize-macos26: credits cleanup
Switched to a new branch 'cleanup-modernization-leftovers'
branch 'cleanup-modernization-leftovers' set up to track 'origin/master'.
==== clean checkout? ====
## cleanup-modernization-leftovers...origin/master
?? .claude/
?? .codex/
?? .entire/
?? .github/
```

> AGENT

Clean. Now cherry-pick the dsa removal and restore the Credits changes.

> TOOL

tool_use Bash
id: toolu_012iffxxbSCKK6tw9sbWCKzk
```json
{
  "command": "git cherry-pick -n 77f5ade && echo \"cherry-pick OK\" && git stash pop && echo \"==== combined changes ====\" && git status -s && echo \"==== diff stat vs master ====\" && git diff --cached --stat; git diff --stat",
  "description": "Apply dsa removal and restore credits changes"
}
```

> TOOL

tool_result
id: toolu_012iffxxbSCKK6tw9sbWCKzk
```
cherry-pick OK
On branch cleanup-modernization-leftovers
Your branch is up to date with 'origin/master'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   Cakebrew.xcodeproj/project.pbxproj
	modified:   Cakebrew/Cakebrew-Info.plist
	deleted:    Cakebrew/dsa_pub.pem

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   Cakebrew/Credits.rtf
	modified:   Cakebrew/pt.lproj/Credits.rtf

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.claude/
	.codex/
	.entire/
	.github/

Dropped refs/stash@{0} (b60a6c59c7c6f21e4314c902164df20db9be1406)
==== combined changes ====
M  Cakebrew.xcodeproj/project.pbxproj
M  Cakebrew/Cakebrew-Info.plist
 M Cakebrew/Credits.rtf
D  Cakebrew/dsa_pub.pem
 M Cakebrew/pt.lproj/Credits.rtf
?? .claude/
?? .codex/
?? .entire/
?? .github/
==== diff stat vs master ====
 Cakebrew.xcodeproj/project.pbxproj |  4 ----
 Cakebrew/Cakebrew-Info.plist       |  8 --------
 Cakebrew/dsa_pub.pem               | 20 --------------------
 3 files changed, 32 deletions(-)
 Cakebrew/Credits.rtf          | 8 --------
 Cakebrew/pt.lproj/Credits.rtf | 4 ----
 2 files changed, 12 deletions(-)
```

> AGENT

All five changes are present and the tooling dirs are correctly excluded. Let me verify it builds, then commit.

> TOOL

tool_use Bash
id: toolu_015phtuBNZrcNcaLmjVmaUVs
```json
{
  "command": "xcodebuild -workspace Cakebrew.xcworkspace -scheme Cakebrew -configuration Debug -destination 'platform=macOS' build 2>&1 | grep -E \"error:|BUILD SUCCEEDED|BUILD FAILED\" | tail -5",
  "description": "Build the consolidation branch",
  "timeout": 420000
}
```

> TOOL

tool_result
id: toolu_015phtuBNZrcNcaLmjVmaUVs
```
** BUILD SUCCEEDED ** [4.339 sec]
```

> AGENT

Build passes. Committing all five changes, pushing, and opening the PR against `master`.

> TOOL

tool_use Bash
id: toolu_01RGcNL5AG2K4DuJ5aXDkSBp
```json
{
  "command": "git add Cakebrew.xcodeproj/project.pbxproj Cakebrew/Cakebrew-Info.plist Cakebrew/dsa_pub.pem Cakebrew/Credits.rtf Cakebrew/pt.lproj/Credits.rtf && \\\ngit commit -m \"$(cat <<'EOF'\nRemove leftover Sparkle DSA key and stale PXSourceList credits\n\nFinishes the modernization cleanup:\n- Delete dsa_pub.pem and remove its project/resource references plus the\n  leftover Sparkle keys from Cakebrew-Info.plist (Sparkle is gone).\n- Drop the PXSourceList attribution from Credits.rtf / pt.lproj/Credits.rtf\n  now that the sidebar uses native NSOutlineView.\n\nCo-Authored-By: Claude Opus 4.7 (1M context) <<REDACTED_EMAIL>>\nEOF\n)\" && git push -u origin cleanup-modernization-leftovers 2>&1 | tail -4",
  "description": "Commit and push the consolidation branch"
}
```

> TOOL

tool_result ERROR
id: toolu_01RGcNL5AG2K4DuJ5aXDkSBp
```
Exit code 128
fatal: pathspec 'Cakebrew/dsa_pub.pem' did not match any files
```

> AGENT

The dsa deletion is already staged from the cherry-pick — I just need to add the two Credits files. Re-running:

> TOOL

tool_use Bash
id: toolu_012Y1NfUJeBcapKyCc8ZPxaj
```json
{
  "command": "git add Cakebrew/Credits.rtf Cakebrew/pt.lproj/Credits.rtf && echo \"==== staged ====\" && git status -s && git commit -m \"$(cat <<'EOF'\nRemove leftover Sparkle DSA key and stale PXSourceList credits\n\nFinishes the modernization cleanup:\n- Delete dsa_pub.pem and remove its project/resource references plus the\n  leftover Sparkle keys from Cakebrew-Info.plist (Sparkle is gone).\n- Drop the PXSourceList attribution from Credits.rtf / pt.lproj/Credits.rtf\n  now that the sidebar uses native NSOutlineView.\n\nCo-Authored-By: Claude Opus 4.7 (1M context) <<REDACTED_EMAIL>>\nEOF\n)\" && git push -u origin cleanup-modernization-leftovers 2>&1 | tail -4",
  "description": "Stage credits, commit, and push the branch"
}
```

> TOOL

tool_result
id: toolu_012Y1NfUJeBcapKyCc8ZPxaj
```
==== staged ====
M  Cakebrew.xcodeproj/project.pbxproj
M  Cakebrew/Cakebrew-Info.plist
M  Cakebrew/Credits.rtf
D  Cakebrew/dsa_pub.pem
M  Cakebrew/pt.lproj/Credits.rtf
?? .claude/
?? .codex/
?? .entire/
?? .github/
[cleanup-modernization-leftovers f07329b] Remove leftover Sparkle DSA key and stale PXSourceList credits
 5 files changed, 44 deletions(-)
 delete mode 100644 Cakebrew/dsa_pub.pem
remote: 
To https://github.com/scottdensmore/Cakebrew.git
 * [new branch]      cleanup-modernization-leftovers -> cleanup-modernization-leftovers
branch 'cleanup-modernization-leftovers' set up to track 'origin/cleanup-modernization-leftovers'.
```

> AGENT

Pushed as `f07329b` with all five changes (tooling dirs excluded). Creating the PR against `master`.

> TOOL

tool_use Bash
id: toolu_01EZavg8zqBTXuZuRv6AZacL
```json
{
  "command": "gh pr create --repo scottdensmore/Cakebrew --base master --head cleanup-modernization-leftovers --title \"Remove leftover Sparkle DSA key and stale PXSourceList credits\" --body \"$(cat <<'EOF'\n## Summary\nFinishes the macOS 26 modernization cleanup, landing two leftovers directly on `master`:\n- **Sparkle DSA key** — deletes `dsa_pub.pem`, its `project.pbxproj` build/resource references, and the leftover Sparkle keys in `Cakebrew-Info.plist`. Sparkle itself was already removed.\n- **PXSourceList credits** — removes the now-stale PXSourceList attribution from `Credits.rtf` and `pt.lproj/Credits.rtf`, since the sidebar is now native `NSOutlineView`.\n\n## Context\nThe dsa-key removal had previously been merged into the `modernize-macos26` branch (PR #2) rather than `master`, and the credits cleanup was uncommitted. This branch was cut fresh from `master` and contains only the net remaining diff, so it merges cleanly.\n\n## Test plan\n- [x] `xcodebuild -workspace Cakebrew.xcworkspace -scheme Cakebrew` → BUILD SUCCEEDED\n- [x] Deletions only; no behavior change\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)\nEOF\n)\" 2>&1 | tail -3",
  "description": "Create the consolidation PR against master"
}
```

> TOOL

tool_result
id: toolu_01EZavg8zqBTXuZuRv6AZacL
```
https://github.com/scottdensmore/Cakebrew/pull/3
```

> AGENT

PR #3 is up: **[Remove leftover Sparkle DSA key and stale PXSourceList credits](https://github.com/scottdensmore/Cakebrew/pull/3)**.

## Answer to your question
It wasn't ready before — but it is now. To recap what I found and fixed:
- ❌ The dsa-key removal (PR #2) had merged into `modernize-macos26`, **not** `master`.
- ❌ The Credits cleanup was uncommitted.
- ✅ I cut a clean branch off `master` with exactly the net remaining diff (5 files, deletions only), verified **BUILD SUCCEEDED**, and opened PR #3. It merges cleanly with no divergence/conflict risk.

PR #3 is ready to merge. How do you want to finish it?

> TOOL

tool_use AskUserQuestion
id: toolu_016cBbBNPe94Yn3JurDtmHUT
```json
{
  "questions": [
    {
      "question": "How should I finish PR #3?",
      "header": "Finish PR #3",
      "multiSelect": false,
      "options": [
        {
          "label": "Squash-merge now",
          "description": "Merge PR #3 into master immediately. It's deletions-only and the build passes, so low risk."
        },
        {
          "label": "Run Copilot review first",
          "description": "Request a Copilot review on PR #3 (as we did for #1), address anything actionable, then squash-merge."
        },
        {
          "label": "Leave it for me to review",
          "description": "Stop here; you'll review and merge PR #3 yourself."
        }
      ]
    }
  ]
}
```

> TOOL

tool_result
id: toolu_016cBbBNPe94Yn3JurDtmHUT
```
Your questions have been answered: "How should I finish PR #3?"="Run Copilot review first". You can now continue with these answers in mind.
```

> AGENT

Requesting a Copilot review on PR #3. Let me get its node ID and trigger the review.

> TOOL

tool_use Bash
id: toolu_01AuhExNr9Y8Gq6D8aK1SN5H
```json
{
  "command": "PRID=$(gh api graphql -f query='query { repository(owner:\"scottdensmore\", name:\"Cakebrew\"){ pullRequest(number:3){ id } } }' --jq '.data.repository.pullRequest.id'); echo \"PR3 id: $PRID\"; gh api graphql -f query=\"mutation { requestReviews(input: {pullRequestId: \\\"$PRID\\\", botIds: [\\\"BOT_kgDOCnlnWA\\\"], union: true}) { pullRequest { reviewRequests(first:5){ nodes { requestedReviewer { __typename ... on Bot { login } } } } } } }\" --jq '.data.requestReviews.pullRequest.reviewRequests.nodes[].requestedReviewer.login'",
  "description": "Get PR #3 node id and request Copilot review"
}
```

> TOOL

tool_result
id: toolu_01AuhExNr9Y8Gq6D8aK1SN5H
```
PR3 id: PR_kwDOA4x9PM7fQLLh
copilot-pull-request-reviewer
```

> AGENT

Copilot review requested on PR #3. Setting up the background watcher for its review to land.

> TOOL

tool_use Bash
id: toolu_01CjcdHStpA5mZs8GMqTBqTu
```json
{
  "command": "until [ \"$(gh pr view 3 --repo scottdensmore/Cakebrew --json reviews --jq '[.reviews[] | select(.author.login==\"copilot-pull-request-reviewer\")] | length')\" -ge 1 ]; do sleep 15; done; echo \"Copilot review on PR #3 has landed\"",
  "description": "Poll until Copilot reviews PR #3",
  "run_in_background": true
}
```

> TOOL

tool_result
id: toolu_01CjcdHStpA5mZs8GMqTBqTu
```
Command running in background with ID: bqwd7f2p7. Output is being written to: /private/tmp/claude-501/-Users-scottdensmore-Developer-scottdensmore-cakebrew/00a7d348-fdab-4cac-8b78-0fd30c4f09b7/tasks/bqwd7f2p7.output. You will be notified when it completes. To check interim output, use Read on that file path.
```

> AGENT

Copilot review requested on PR #3 and I'm watching for it in the background. When it lands I'll pull any findings, fix + reply/resolve anything actionable (flagging anything that needs your judgment), and then squash-merge into `master`. I'll report back when it posts.

> AGENT

The review landed. Let me pull its findings.

> TOOL

tool_use Bash
id: toolu_01Ck3zwgAMakm2nQrP8XgZcU
```json
{
  "command": "echo \"==== Copilot review body ====\"; gh pr view 3 --repo scottdensmore/Cakebrew --json reviews --jq '[.reviews[] | select(.author.login==\"copilot-pull-request-reviewer\")] | last | {at:.submittedAt, state:.state, body:.body}'; echo; echo \"==== unresolved threads on PR #3 ====\"; gh api graphql -f query='\nquery {\n  repository(owner: \"scottdensmore\", name: \"Cakebrew\") {\n    pullRequest(number: 3) {\n      reviewThreads(first: 50) {\n        nodes { id isResolved\n          comments(first: 10) { nodes { databaseId author { login } path originalLine body } } }\n      }\n    }\n  }\n}' --jq '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved==false) | {threadId:.id, comments:[.comments.nodes[]|{id:.databaseId, user:.author.login, path:.path, line:.originalLine, body:.body}]}'",
  "description": "Fetch Copilot review and unresolved threads on PR #3"
}
```

> TOOL

tool_result
id: toolu_01Ck3zwgAMakm2nQrP8XgZcU
```
==== Copilot review body ====
{"at":"2026-05-26T03:41:06Z","body":"## Pull request overview\n\nThis PR finishes macOS modernization cleanup by removing dead Sparkle update-signing artifacts and outdated third‑party credits that no longer apply now that the sidebar uses native `NSOutlineView`.\n\n**Changes:**\n- Deleted the leftover Sparkle DSA public key file and removed its Xcode project resource references.\n- Removed stale Sparkle `SU*` keys from `Cakebrew-Info.plist`.\n- Removed outdated PXSourceList attribution from Credits (English + Portuguese localization).\n\n### Reviewed changes\n\nCopilot reviewed 5 out of 5 changed files in this pull request and generated no comments.\n\n\u003cdetails\u003e\n\u003csummary\u003eShow a summary per file\u003c/summary\u003e\n\n| File | Description |\r\n| ---- | ----------- |\r\n| `Cakebrew/pt.lproj/Credits.rtf` | Removes obsolete PXSourceList attribution from localized credits. |\r\n| `Cakebrew/dsa_pub.pem` | Deletes unused Sparkle DSA public key file. |\r\n| `Cakebrew/Credits.rtf` | Removes obsolete PXSourceList attribution from main credits. |\r\n| `Cakebrew/Cakebrew-Info.plist` | Removes unused Sparkle `SU*` plist keys. |\r\n| `Cakebrew.xcodeproj/project.pbxproj` | Removes `dsa_pub.pem` file/resource references from the Xcode project. |\n\u003c/details\u003e\n\n\n\n\n\n\n\n---\n\n💡 \u003ca href=\"/scottdensmore/Cakebrew/new/master?filename=.github/instructions/*.instructions.md\" class=\"Link--inTextBlock\" target=\"_blank\" rel=\"noopener noreferrer\"\u003eAdd Copilot custom instructions\u003c/a\u003e for smarter, more guided reviews. \u003ca href=\"https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot\" class=\"Link--inTextBlock\" target=\"_blank\" rel=\"noopener noreferrer\"\u003eLearn how to get started\u003c/a\u003e.","state":"COMMENTED"}

==== unresolved threads on PR #3 ====
```

> AGENT

Copilot reviewed all 5 files and generated **zero comments** — clean. No threads to address. Proceeding to squash-merge PR #3 into `master`.

> TOOL

tool_use Bash
id: toolu_019C4ao99RuPrdJpVGFP78TC
```json
{
  "command": "gh pr merge 3 --repo scottdensmore/Cakebrew --squash 2>&1 | tail -5; echo \"==== PR #3 state ====\"; gh pr view 3 --repo scottdensmore/Cakebrew --json state,mergedAt,mergeCommit --jq '{state, mergedAt, mergeCommit:.mergeCommit.oid}'; echo \"==== origin/master now ====\"; git fetch origin --quiet && git log --oneline origin/master -4",
  "description": "Squash-merge PR #3 and confirm master state"
}
```

> TOOL

tool_result
id: toolu_019C4ao99RuPrdJpVGFP78TC
```
==== PR #3 state ====
{"mergeCommit":"bd33d22c138238ad56fb8e1b0493d6b72ab2309d","mergedAt":"2026-05-26T03:46:56Z","state":"MERGED"}
==== origin/master now ====
bd33d22 Remove leftover Sparkle DSA key and stale PXSourceList credits (#3)
f755a5c Modernize for macOS 26: drop Sparkle & PXSourceList
1053fe6 Bump build to 594
56eac5c Revert fix for Sidebar
```

> AGENT

PR #3 is merged. `master` is now `bd33d22` and contains the complete modernization. Let me do a final sanity check that everything actually landed on `master`.

> TOOL

tool_use Bash
id: toolu_01E8TohSxoRhi2vBF6EgsoDZ
```json
{
  "command": "echo \"==== dsa_pub.pem on origin/master? ====\"; git ls-tree origin/master -- Cakebrew/dsa_pub.pem | grep -q . && echo \"STILL PRESENT (bad)\" || echo \"gone (good)\"; echo \"==== PXSourceList in credits on origin/master? ====\"; git show origin/master:Cakebrew/Credits.rtf | grep -c \"PXSourceList\" | sed 's/^/Credits.rtf matches: /'; echo \"==== PXSourceList anywhere in source on origin/master? ====\"; git grep -l \"PXSourceList\" origin/master -- '*.h' '*.m' '*.xib' '*.pbxproj' 2>/dev/null || echo \"none in code/project\"; echo \"==== branches merged into origin/master ====\"; git branch -r --merged origin/master | grep -vE \"HEAD\" ",
  "description": "Verify master has all cleanup and list merged remote branches"
}
```

> TOOL

tool_result
id: toolu_01E8TohSxoRhi2vBF6EgsoDZ
```
==== dsa_pub.pem on origin/master? ====
gone (good)
==== PXSourceList in credits on origin/master? ====
Credits.rtf matches: 0
==== PXSourceList anywhere in source on origin/master? ====
none in code/project
==== branches merged into origin/master ====
  origin/dev
  origin/master
  upstream/dependents-listing
  upstream/feature/big-sur-interface-changes
  upstream/fix/brew-formulae-10.8
  upstream/main
  upstream/stable
```

> AGENT

Everything's verified on `master`: `dsa_pub.pem` gone, zero PXSourceList references in code/project/credits.

## All done ✅

PR #3 squash-merged into `master` (`bd33d22`) after a **clean Copilot review (0 comments)**. The full macOS 26 modernization is now complete and consolidated on `master`:

- `f755a5c` — drop Sparkle & PXSourceList, native `NSOutlineView` sidebar
- `bd33d22` — remove leftover Sparkle DSA key + stale PXSourceList credits

**What I had to untangle this round:** the dsa-removal task (PR #2) had merged into the wrong base (`modernize-macos26`), and the Credits cleanup was uncommitted — so neither was on `master`. I cut a fresh branch off `master` with just the net diff, got a clean Copilot pass, and merged. No divergence or conflicts.

## Loose ends you may want to tidy (all optional, all merged/obsolete now)
A few branches are now fully superseded by `master`:
- `cleanup-modernization-leftovers` (PR #3 head — merged)
- `modernize-macos26` (PR #1 squashed to master; also where PR #2 landed)
- `remove-sparkle-dsa-key` (PR #2 head)

And your **local checkout is on `cleanup-modernization-leftovers`**, with local `master` behind origin.

Want me to:
1. **Switch to `master` and fast-forward** it to `origin/master`, and
2. **Delete those three obsolete branches** (local + remote)?

I won't run any […]

> DEVELOPER

Yes do both

> AGENT

Confirmed. I'll switch to `master`, fast-forward it, then delete the obsolete branches. First, let me switch + fast-forward and check for anything (like leftover worktrees) that could block branch deletion.

> TOOL

tool_use Bash
id: toolu_01PwzWtNnaSWkeTWooJVes6X
```json
{
  "command": "git checkout master && git merge --ff-only origin/master && echo \"==== master now ====\" && git log --oneline -2; echo \"==== worktrees ====\"; git worktree list; echo \"==== local branches ====\"; git branch; echo \"==== remote branches to delete (exist?) ====\"; git ls-remote --heads origin modernize-macos26 cleanup-modernization-leftovers remove-sparkle-dsa-key",
  "description": "Switch to master, fast-forward, and inventory branches/worktrees"
}
```

> TOOL

tool_result
id: toolu_01PwzWtNnaSWkeTWooJVes6X
```
<persisted-output>
Output too large (38.3KB). Full output saved to: /home/<USER>/.claude/projects/-Users-scottdensmore-Developer-scottdensmore-cakebrew/86f7230f-16a2-4201-9dae-105c1789c2c6/tool-results/bp7ql773l.txt

Preview (first 2KB):
Switched to branch 'master'
Your branch is behind 'origin/master' by 2 commits, and can be fast-forwarded.
  (use "git pull" to update your local branch)
Updating 1053fe6..bd33d22
Fast-forward
 .gitignore                                         |    4 +
 .gitmodules                                        |    3 -
 Cakebrew.xcodeproj/project.pbxproj                 |  101 +-
 .../xcshareddata/xcschemes/Cakebrew.xcscheme       |    2 +-
 .../xcshareddata/xcschemes/CakebrewTests.xcscheme  |    2 +-
 Cakebrew.xcworkspace/contents.xcworkspacedata      |    3 -
 Cakebrew/BPAppDelegate.m                           |   56 +-
 Cakebrew/BPFormulaeTableView.m                     |    2 +-
 Cakebrew/BPHomebrewManager.m                       |   34 +-
 Cakebrew/BPToolbar.m                               |    6 +-
 Cakebrew/Base.lproj/MainMenu.xib                   |   41 +-
 Cakebrew/Cakebrew-Info.plist                       |    8 -
 Cakebrew/Controllers/BPHomebrewViewController.h    |    1 -
 Cakebrew/Controllers/BPSideBarController.h         |   34 +-
 Cakebrew/Controllers/BPSideBarController.m         |  272 +-
 Cakebrew/Credits.rtf                               |    8 -
 Cakebrew/Frameworks/Sparkle.framework/Headers      |    1 -
 Cakebrew/Frameworks/Sparkle.framework/Modules      |    1 -
 .../Frameworks/Sparkle.framework/PrivateHeaders    |    1 -
 Cakebrew/Frameworks/Sparkle.framework/Resources    |    1 -
 Cakebrew/Frameworks/Sparkle.framework/Sparkle      |    1 -
 .../Versions/A/Headers/SPUDownloadData.h           |   43 -
 .../Versions/A/Headers/SPUDownloader.h             |   25 -
 .../Versions/A/Headers/SPUDownloaderDelegate.h     |   38 -
 .../Versions/A/Headers/SPUDownloaderProtocol.h     |   34 -
 .../Versions/A/Headers/SPUDownloaderSession.h      |   20 -
 .../Versions/A/Headers/SPUURLRequest.h             |   35 -
 .../Versions/A/Headers/SUAppcast.h                 |   31 -
 .../Versions/A/Headers/SUAppcastItem.h             |   55 -
...
</persisted-output>
```

> AGENT

Master fast-forwarded successfully. The diff stat was huge; let me get just the branch/worktree inventory I need.

> TOOL

tool_use Bash
id: toolu_01Cp8Br7bUAHPwHa9e6des4d
```json
{
  "command": "echo \"==== current ====\"; git branch --show-current; echo \"==== worktrees ====\"; git worktree list; echo \"==== local branches ====\"; git branch; echo \"==== remote branches (targets) ====\"; git ls-remote --heads origin modernize-macos26 cleanup-modernization-leftovers remove-sparkle-dsa-key",
  "description": "Concise inventory of worktrees and branches"
}
```

> TOOL

tool_result
id: toolu_01Cp8Br7bUAHPwHa9e6des4d
```
==== current ====
master
==== worktrees ====
/home/<USER>/Developer/scottdensmore/cakebrew bd33d22 [master]
==== local branches ====
  cleanup-modernization-leftovers
  entire/checkpoints/v1
  entire/f07329b-e3b0c4
* master
  modernize-macos26
==== remote branches (targets) ====
f07329b31fa240e7d24646e41fde0a1cb707bf75	refs/heads/cleanup-modernization-leftovers
77f5ade1e1feb1553a52dd89618774c1daa062f2	refs/heads/modernize-macos26
```

> AGENT

Inventory is clean — only the main worktree, so nothing blocks deletion. Notes:
- `remove-sparkle-dsa-key` no longer exists locally or on origin (it was auto-deleted when PR #2 merged), so nothing to do there.
- The `entire/*` branches are tooling checkpoints — I'll leave those untouched.

Deleting the two real obsolete branches (`modernize-macos26`, `cleanup-modernization-leftovers`) locally and on origin. Both are squash-merged, so I'll force the local delete.

> TOOL

tool_use Bash
id: toolu_012VmcRuEYhNpGyfuDv1LHa3
```json
{
  "command": "echo \"==== delete local ====\"; git branch -D modernize-macos26 cleanup-modernization-leftovers; echo \"==== delete remote ====\"; git push origin --delete modernize-macos26 cleanup-modernization-leftovers 2>&1 | tail -6",
  "description": "Delete the two obsolete branches locally and on origin"
}
```

> TOOL

tool_result
id: toolu_012VmcRuEYhNpGyfuDv1LHa3
```
==== delete local ====
Deleted branch modernize-macos26 (was 77f5ade).
Deleted branch cleanup-modernization-leftovers (was f07329b).
==== delete remote ====
[entire] Pushing entire/checkpoints/v1 to origin..... done
To https://github.com/scottdensmore/Cakebrew.git
 - [deleted]         cleanup-modernization-leftovers
 - [deleted]         modernize-macos26
```

> AGENT

Done. Let me confirm the final state.

> TOOL

tool_use Bash
id: toolu_01XXMwqHkavuwvtnUHAZ1FMd
```json
{
  "command": "echo \"==== local branches ====\"; git branch; echo \"==== remote branches ====\"; git ls-remote --heads origin | awk '{print $2}' | sed 's#refs/heads/##'; echo \"==== master status ====\"; git status -sb | head -1",
  "description": "Verify final branch state"
}
```

> TOOL

tool_result
id: toolu_01XXMwqHkavuwvtnUHAZ1FMd
```
==== local branches ====
  entire/checkpoints/v1
  entire/f07329b-e3b0c4
* master
==== remote branches ====
appcenter
dev
entire/checkpoints/v1
install-homebrew
master
wip
==== master status ====
## master...origin/master
```

> AGENT

All cleaned up. Final state:

- **On `master`**, fully in sync with `origin/master` (`bd33d22`) — nothing pending.
- **Obsolete branches deleted** (local + remote): `modernize-macos26`, `cleanup-modernization-leftovers`. (`remove-sparkle-dsa-key` was already gone.)
- Remaining branches are your pre-existing ones (`appcenter`, `dev`, `install-homebrew`, `wip`) plus the `entire/*` tooling checkpoints — all left untouched.

## Wrap-up of the whole effort
The macOS 26 modernization is complete and consolidated on `master` across two merged PRs:
- **PR #1** (`f755a5c`) — dropped Sparkle & PXSourceList, migrated the sidebar to a native `NSOutlineView`, plus the review fixes (bundle IDs, cache decode, notifications, etc.).
- **PR #3** (`bd33d22`) — removed the leftover Sparkle DSA key and stale PXSourceList credits; passed a clean Copilot review.

The original build break (missing PXSourceList) is fixed, the app builds and runs, and your branch list is tidy. You're good to go.

> DEVELOPER

I added entire to the project so we need to check in those changes

> AGENT

Before committing, let me see exactly what "entire" added so I commit the right files (and not user-specific data or secrets).

> TOOL

tool_use Bash
id: toolu_01CgLp97bfaSePDPHKsepwi4
```json
{
  "command": "echo \"==== git status ====\"; git status --short; echo; echo \"==== .entire/ tree ====\"; find .entire -maxdepth 3 2>/dev/null | head -50; echo; echo \"==== sizes ====\"; du -sh .entire .claude .codex .github 2>/dev/null",
  "description": "Inspect untracked entire/tooling dirs and sizes"
}
```

> TOOL

tool_result
id: toolu_01CgLp97bfaSePDPHKsepwi4
```
==== git status ====
?? .claude/
?? .codex/
?? .entire/
?? .github/

==== .entire/ tree ====
.entire
.entire/settings.json
.entire/logs
.entire/.gitignore
.entire/tmp
.entire/metadata
.entire/logs/entire.log
.entire/tmp/pre-prompt-86f7230f-16a2-4201-9dae-105c1789c2c6.json
.entire/metadata/86f7230f-16a2-4201-9dae-105c1789c2c6
.entire/metadata/c5508f23-68ad-4ad4-aaa7-d78ccbc9f10a
.entire/metadata/ff0f4123-0c71-4068-92ca-4e7a2399c8d7
.entire/metadata/86f7230f-16a2-4201-9dae-105c1789c2c6/full.jsonl
.entire/metadata/86f7230f-16a2-4201-9dae-105c1789c2c6/prompt.txt
.entire/metadata/c5508f23-68ad-4ad4-aaa7-d78ccbc9f10a/full.jsonl
.entire/metadata/ff0f4123-0c71-4068-92ca-4e7a2399c8d7/full.jsonl

==== sizes ====
1.9M	.entire
 12K	.claude
 12K	.codex
4.0K	.github
```

> AGENT

`.entire/` ships its own `.gitignore`, so git will honor it. Let me read what entire intends to track vs ignore, and peek at the other untracked dirs.

> TOOL

tool_use Read
id: toolu_01T6KSh7UNJWmPh6SBHWAFaC
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/.entire/.gitignore"
}
```

> TOOL

tool_result
id: toolu_01T6KSh7UNJWmPh6SBHWAFaC
```
1	tmp/
2	settings.local.json
3	metadata/
4	logs/
5	redactors/local/
6	
```

> TOOL

tool_use Read
id: toolu_01MdUy2YB91W7FkLoz7sRfjM
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/.entire/settings.json"
}
```

> TOOL

tool_result
id: toolu_01MdUy2YB91W7FkLoz7sRfjM
```
1	{
2	  "enabled": true,
3	  "telemetry": true
4	}
5	
```

> TOOL

tool_use Bash
id: toolu_01PhTGx3kGucyP6DPxYjr7he
```json
{
  "command": "echo \"==== git add dry-run for .entire ====\"; git add -n .entire/ 2>&1; echo; echo \"==== .github contents ====\"; find .github -type f 2>/dev/null; echo \"==== .claude contents ====\"; find .claude -type f 2>/dev/null; echo \"==== .codex contents ====\"; find .codex -type f 2>/dev/null",
  "description": "Dry-run entire add and list other tooling dir contents"
}
```

> TOOL

tool_result
id: toolu_01PhTGx3kGucyP6DPxYjr7he
```
==== git add dry-run for .entire ====
add '.entire/.gitignore'
add '.entire/settings.json'

==== .github contents ====
.github/hooks/entire.json
==== .claude contents ====
.claude/settings.json
.claude/settings.local.json
.claude/agents/entire-search.md
==== .codex contents ====
.codex/hooks.json
.codex/config.toml
.codex/agents/entire-search.toml
```

> AGENT

`entire` added integration files across several dirs (`.entire/`, `.github/hooks/`, `.claude/`, `.codex/`). Let me read the ambiguous ones to confirm they're shareable config and not user-local data or secrets — particularly `settings.local.json`, which by convention should stay out of git.

> TOOL

tool_use Read
id: toolu_01WVcNER8i8nqNWzWDJAMc4Z
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/.claude/settings.json"
}
```

> TOOL

tool_result
id: toolu_01WVcNER8i8nqNWzWDJAMc4Z
```
1	{
2	  "hooks": {
3	    "PostToolUse": [
4	      {
5	        "matcher": "Task",
6	        "hooks": [
7	          {
8	            "type": "command",
9	            "command": "sh -c 'if ! command -v entire >/dev/null 2>&1; then exit 0; fi; exec entire hooks claude-code post-task'"
10	          }
11	        ]
12	      },
13	      {
14	        "matcher": "TodoWrite",
15	        "hooks": [
16	          {
17	            "type": "command",
18	            "command": "sh -c 'if ! command -v entire >/dev/null 2>&1; then exit 0; fi; exec entire hooks claude-code post-todo'"
19	          }
20	        ]
21	      }
22	    ],
23	    "PreToolUse": [
24	      {
25	        "matcher": "Task",
26	        "hooks": [
27	          {
28	            "type": "command",
29	            "command": "sh -c 'if ! command -v entire >/dev/null 2>&1; then exit 0; fi; exec entire hooks claude-code pre-task'"
30	          }
31	        ]
32	      }
33	    ],
34	    "SessionEnd": [
35	      {
36	        "matcher": "",
37	        "hooks": [
38	          {
39	            "type": "command",
40	            "command": "sh -c 'if ! command -v entire >/dev/null 2>&1; then exit 0; fi; exec entire hooks claude-code session-end'"
41	          }
42	        ]
43	      }
44	    ],
45	    "SessionStart": [
46	      {
47	        "matcher": "",
48	        "hooks": [
49	          {
50	            "type": "command",
51	            "command": "sh -c […]

> TOOL

tool_use Read
id: toolu_01CHmMNfifF8YLe7rr9DGCxk
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/.claude/settings.local.json"
}
```

> TOOL

tool_result
id: toolu_01CHmMNfifF8YLe7rr9DGCxk
```
1	{
2	  "permissions": {
3	    "allow": [
4	      "Bash(git submodule *)",
5	      "Bash(git ls-tree *)",
6	      "Bash(echo \"EXIT: $?\")",
7	      "Bash(xcodebuild -workspace Cakebrew.xcworkspace -scheme Cakebrew -configuration Debug -destination 'platform=macOS' build)",
8	      "Bash(open /home/<USER>/Library/Developer/Xcode/DerivedData/Cakebrew-ejkvoljwklzjefduqadkgzlgzyoq/Build/Products/Debug/Cakebrew.app)"
9	    ]
10	  }
11	}
12	
```

> TOOL

tool_use Read
id: toolu_01D26FwieeCsDiPk6tL1VYaE
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/.codex/config.toml"
}
```

> TOOL

tool_result
id: toolu_01D26FwieeCsDiPk6tL1VYaE
```
1	
2	[features]
3	hooks = true
4	
```

> TOOL

tool_use Read
id: toolu_012JPNSxXyUuqC3EJ8C6Wmu8
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/.codex/hooks.json"
}
```

> TOOL

tool_result
id: toolu_012JPNSxXyUuqC3EJ8C6Wmu8
```
1	{
2	  "hooks": {
3	    "PostToolUse": [
4	      {
5	        "matcher": null,
6	        "hooks": [
7	          {
8	            "type": "command",
9	            "command": "sh -c 'if ! command -v entire >/dev/null 2>&1; then exit 0; fi; exec entire hooks codex post-tool-use'",
10	            "timeout": 30
11	          }
12	        ]
13	      }
14	    ],
15	    "SessionStart": [
16	      {
17	        "matcher": null,
18	        "hooks": [
19	          {
20	            "type": "command",
21	            "command": "sh -c 'if ! command -v entire >/dev/null 2>&1; then printf \"%s\\n\" \"{\\\"systemMessage\\\":\\\"Entire CLI is enabled but not installed or not on PATH. Installation guide: https://docs.entire.io/cli/installation#installation-methods\\\"}\"; exit 0; fi; exec entire hooks codex session-start'",
22	            "timeout": 30
23	          }
24	        ]
25	      }
26	    ],
27	    "Stop": [
28	      {
29	        "matcher": null,
30	        "hooks": [
31	          {
32	            "type": "command",
33	            "command": "sh -c 'if ! command -v entire >/dev/null 2>&1; then exit 0; fi; exec entire hooks codex stop'",
34	            "timeout": 30
35	          }
36	        ]
37	      }
38	    ],
39	    "UserPromptSubmit": [
40	      {
41	        "matcher": null,
42	        "hooks": [
43	          {
44	            "type": "command",
45	            "command": "sh -c 'if ! command -v entire >/dev/null 2>&1; then exit 0; fi; exec entire hooks […]

> TOOL

tool_result
id: toolu_01SC5KHF7EugmMeRPbcThhpq
```
1	{
2	  "hooks": {
3	    "agentStop": [
4	      {
5	        "type": "command",
6	        "bash": "sh -c 'if ! command -v entire >/dev/null 2>&1; then exit 0; fi; exec entire hooks copilot-cli agent-stop'",
7	        "comment": "Entire CLI"
8	      }
9	    ],
10	    "errorOccurred": [
11	      {
12	        "type": "command",
13	        "bash": "sh -c 'if ! command -v entire >/dev/null 2>&1; then exit 0; fi; exec entire hooks copilot-cli error-occurred'",
14	        "comment": "Entire CLI"
15	      }
16	    ],
17	    "postToolUse": [
18	      {
19	        "type": "command",
20	        "bash": "sh -c 'if ! command -v entire >/dev/null 2>&1; then exit 0; fi; exec entire hooks copilot-cli post-tool-use'",
21	        "comment": "Entire CLI"
22	      }
23	    ],
24	    "preToolUse": [
25	      {
26	        "type": "command",
27	        "bash": "sh -c 'if ! command -v entire >/dev/null 2>&1; then exit 0; fi; exec entire hooks copilot-cli pre-tool-use'",
28	        "comment": "Entire CLI"
29	      }
30	    ],
31	    "sessionEnd": [
32	      {
33	        "type": "command",
34	        "bash": "sh -c 'if ! command -v entire >/dev/null 2>&1; then exit 0; fi; exec entire hooks copilot-cli session-end'",
35	        "comment": "Entire CLI"
36	      }
37	    ],
38	    "sessionStart": [
39	      {
40	        "type": "command",
41	        "bash": "sh […]

> TOOL

tool_use Read
id: toolu_01SC5KHF7EugmMeRPbcThhpq
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/.github/hooks/entire.json"
}
```

> AGENT

All clear. These are all `entire` integration hooks (each guards with `command -v entire`, so they safely no-op for contributors who don't have it). The one file I'll **exclude** is `.claude/settings.local.json` — it's machine-specific (your home paths, DerivedData) and by convention should stay out of git.

Per your branch → PR → squash workflow, I'll do this on a branch. Let me create it and read the current `.gitignore`.

> TOOL

tool_use Bash
id: toolu_01UkGUdj7DKWZAPFMwVFosTG
```json
{
  "command": "git checkout -b add-entire-integration && echo \"---- created ----\"",
  "description": "Create branch for the entire integration commit"
}
```

> TOOL

tool_use Read
id: toolu_01GFLy1mGm3U5KLGkhUaLRXu
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/.gitignore",
  "offset": 15,
  "limit": 10
}
```

> TOOL

tool_result
id: toolu_01UkGUdj7DKWZAPFMwVFosTG
```
Switched to a new branch 'add-entire-integration'
---- created ----
```

> TOOL

tool_result
id: toolu_01GFLy1mGm3U5KLGkhUaLRXu
```
15	*.moved-aside
16	DerivedData
17	*.xcuserstate
18	
19	
20	### Genkit ###
21	.genkit/
22	
23	
24	### OSX ###
```

> TOOL

tool_result
id: toolu_01HLSP4NGcvY6VF3Lzrd1Fzn
```
The file /home/<USER>/Developer/scottdensmore/cakebrew/.gitignore has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now I'll add the local-settings ignore rule, then commit only the shared entire files.

> TOOL

tool_use Edit
id: toolu_01HLSP4NGcvY6VF3Lzrd1Fzn
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/.gitignore",
  "old_string": "### Genkit ###\n.genkit/\n\n\n### OSX ###",
  "new_string": "### Genkit ###\n.genkit/\n\n\n### Claude Code (machine-local settings) ###\n.claude/settings.local.json\n\n\n### OSX ###"
}
```

> TOOL

tool_use Bash
id: toolu_019o3iwCq6unKk7S5daDHtae
```json
{
  "command": "git add .gitignore .entire/.gitignore .entire/settings.json .github/hooks/entire.json .claude/settings.json .claude/agents/entire-search.md .codex/config.toml .codex/hooks.json .codex/agents/entire-search.toml && echo \"==== staged (verify settings.local.json is NOT here) ====\" && git status --short",
  "description": "Stage shared entire files plus gitignore, excluding local settings"
}
```

> TOOL

tool_result
id: toolu_019o3iwCq6unKk7S5daDHtae
```
==== staged (verify settings.local.json is NOT here) ====
A  .claude/agents/entire-search.md
A  .claude/settings.json
A  .codex/agents/entire-search.toml
A  .codex/config.toml
A  .codex/hooks.json
A  .entire/.gitignore
A  .entire/settings.json
A  .github/hooks/entire.json
M  .gitignore
```

> AGENT

Exactly right — `.claude/settings.local.json` is excluded (now gitignored), and only the shared entire integration files are staged. Committing and pushing.

> TOOL

tool_use Bash
id: toolu_018jTQ6Cr2aRLrdNCZFYnRzv
```json
{
  "command": "git commit -m \"$(cat <<'EOF'\nAdd Entire CLI integration\n\nCheck in the Entire tooling hooks/agents for Claude Code, Codex, and the\nCopilot CLI. All hooks guard on `command -v entire`, so they no-op for\ncontributors who don't have the CLI installed.\n\n- .entire/: enable flag and ignore rules for local logs/metadata\n- .claude/, .codex/, .github/hooks/: entire lifecycle hooks + entire-search agent\n- .gitignore: keep machine-local .claude/settings.local.json out of git\n\nCo-Authored-By: Claude Opus 4.7 (1M context) <<REDACTED_EMAIL>>\nEOF\n)\" && git push -u origin add-entire-integration 2>&1 | tail -4",
  "description": "Commit and push the entire integration branch"
}
```

> TOOL

tool_result
id: toolu_018jTQ6Cr2aRLrdNCZFYnRzv
```
[add-entire-integration c52166a] Add Entire CLI integration
 9 files changed, 261 insertions(+)
 create mode 100644 .claude/agents/entire-search.md
 create mode 100644 .claude/settings.json
 create mode 100644 .codex/agents/entire-search.toml
 create mode 100644 .codex/config.toml
 create mode 100644 .codex/hooks.json
 create mode 100644 .entire/.gitignore
 create mode 100644 .entire/settings.json
 create mode 100644 .github/hooks/entire.json
remote: 
To https://github.com/scottdensmore/Cakebrew.git
 * [new branch]      add-entire-integration -> add-entire-integration
branch 'add-entire-integration' set up to track 'origin/add-entire-integration'.
```

> AGENT

Committed (`c52166a`) and pushed. Opening the PR against `master`.

> TOOL

tool_use Bash
id: toolu_01TagBk9R8A7HRvFADBjTaFN
```json
{
  "command": "gh pr create --repo scottdensmore/Cakebrew --base master --head add-entire-integration --title \"Add Entire CLI integration\" --body \"$(cat <<'EOF'\n## Summary\nChecks in the [Entire](https://docs.entire.io) CLI integration that was added to the project — lifecycle hooks and the `entire-search` agent for Claude Code, Codex, and the Copilot CLI.\n\n- `.entire/` — enable flag (`settings.json`) and ignore rules for local logs/metadata/tmp\n- `.claude/settings.json` + `.claude/agents/entire-search.md` — Claude Code hooks and search agent\n- `.codex/` — Codex hooks, config, and search agent\n- `.github/hooks/entire.json` — Copilot CLI hooks\n- `.gitignore` — keep machine-local `.claude/settings.local.json` out of git\n\n## Notes\n- Every hook guards on `command -v entire`, so it cleanly no-ops for contributors who don't have the CLI installed — no impact on the build or other contributors.\n- Machine-specific `.claude/settings.local.json` and Entire's local logs/metadata are intentionally **not** committed.\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)\nEOF\n)\" 2>&1 | tail -3",
  "description": "Open PR for entire integration"
}
```

> TOOL

tool_result
id: toolu_01TagBk9R8A7HRvFADBjTaFN
```
https://github.com/scottdensmore/Cakebrew/pull/4
```

> AGENT

PR #4 is up: **[Add Entire CLI integration](https://github.com/scottdensmore/Cakebrew/pull/4)** (9 files, config-only).

What I committed and what I deliberately left out:
- ✅ Committed: the shared `entire` hooks/agents for Claude Code, Codex, and Copilot CLI, plus `.entire/settings.json` and a `.gitignore` rule.
- 🚫 Excluded: `.claude/settings.local.json` (machine-specific paths) and `.entire/` logs/metadata/tmp — now gitignored.

This is pure tooling config (no code, no build impact). How do you want to finish it?

> TOOL

tool_use AskUserQuestion
id: toolu_018D3zjmVPMXzn1iDhiSm9b2
```json
{
  "questions": [
    {
      "question": "How should I finish PR #4?",
      "header": "Finish PR #4",
      "multiSelect": false,
      "options": [
        {
          "label": "Squash-merge now",
          "description": "Config-only, no build impact — merge it straight into master."
        },
        {
          "label": "Run Copilot review first",
          "description": "Request a Copilot review (as with prior PRs), then squash-merge. Adds little for config files, but keeps the process consistent."
        },
        {
          "label": "Leave it for me to review",
          "description": "Stop here; you'll review and merge PR #4 yourself."
        }
      ]
    }
  ]
}
```

> TOOL

tool_result
id: toolu_018D3zjmVPMXzn1iDhiSm9b2
```
Your questions have been answered: "How should I finish PR #4?"="Squash-merge now". You can now continue with these answers in mind.
```

> AGENT

Squash-merging PR #4 now.

> TOOL

tool_use Bash
id: toolu_01WziStDENQTkmG64i2DdoXD
```json
{
  "command": "gh pr merge 4 --repo scottdensmore/Cakebrew --squash 2>&1 | tail -3; echo \"==== PR #4 state ====\"; gh pr view 4 --repo scottdensmore/Cakebrew --json state,mergeCommit --jq '{state, mergeCommit:.mergeCommit.oid}'",
  "description": "Squash-merge PR #4"
}
```

> TOOL

tool_result
id: toolu_01WziStDENQTkmG64i2DdoXD
```
==== PR #4 state ====
{"mergeCommit":"049f03e2ee71b87f5d0c865d02e03fc159ef87b6","state":"MERGED"}
```

> AGENT

Merged as `049f03e`. Syncing local `master` and cleaning up the merged branch (same as before).

> TOOL

tool_use Bash
id: toolu_01WQx9JRhHeHZrQZTFF8EMur
```json
{
  "command": "git checkout master && git fetch origin --quiet && git merge --ff-only origin/master && echo \"==== delete merged branch ====\" && git branch -D add-entire-integration && git push origin --delete add-entire-integration 2>&1 | tail -3; echo \"==== final state ====\"; git log --oneline -3; echo \"-- local branches --\"; git branch",
  "description": "Sync master and delete merged entire branch"
}
```

> TOOL

tool_result
id: toolu_01WQx9JRhHeHZrQZTFF8EMur
```
Switched to branch 'master'
Your branch is up to date with 'origin/master'.
Updating bd33d22..049f03e
Fast-forward
 .claude/agents/entire-search.md  | 25 ++++++++++++
 .claude/settings.json            | 84 ++++++++++++++++++++++++++++++++++++++++
 .codex/agents/entire-search.toml | 23 +++++++++++
 .codex/config.toml               |  3 ++
 .codex/hooks.json                | 52 +++++++++++++++++++++++++
 .entire/.gitignore               |  5 +++
 .entire/settings.json            |  4 ++
 .github/hooks/entire.json        | 61 +++++++++++++++++++++++++++++
 .gitignore                       |  4 ++
 9 files changed, 261 insertions(+)
 create mode 100644 .claude/agents/entire-search.md
 create mode 100644 .claude/settings.json
 create mode 100644 .codex/agents/entire-search.toml
 create mode 100644 .codex/config.toml
 create mode 100644 .codex/hooks.json
 create mode 100644 .entire/.gitignore
 create mode 100644 .entire/settings.json
 create mode 100644 .github/hooks/entire.json
==== delete merged branch ====
Deleted branch add-entire-integration (was c52166a).
To https://github.com/scottdensmore/Cakebrew.git
 - [deleted]         add-entire-integration
==== final state ====
049f03e Add Entire CLI integration (#4)
bd33d22 Remove leftover Sparkle DSA key and stale PXSourceList credits (#3)
f755a5c Modernize for macOS 26: drop Sparkle & PXSourceList
-- local branches --
  entire/c52166a-e3b0c4
  entire/checkpoints/v1
* master
```

> AGENT

Done. The Entire CLI integration is checked in and merged.

## Summary
- **PR #4** ([Add Entire CLI integration](https://github.com/scottdensmore/Cakebrew/pull/4)) squash-merged into `master` as `049f03e`.
- Local `master` fast-forwarded; merged branch `add-entire-integration` deleted (local + remote).

**Committed** (9 files, config only): the `entire` lifecycle hooks + `entire-search` agent for Claude Code, Codex, and Copilot CLI, `.entire/settings.json`, and a `.gitignore` rule.

**Intentionally excluded**: `.claude/settings.local.json` (your machine-specific paths) and `.entire/` logs/metadata/tmp — all now gitignored, so they won't get picked up later.

You're on a clean `master` (`049f03e`), in sync with origin. The `entire/*` entries in your local branch list are just that tool's own checkpoint refs — leave them be.

> DEVELOPER

I want to rename the master branch to main and make it default. Then lets make sure everything is in sync with origina and local

> AGENT

Good idea. I'll use GitHub's built-in **rename branch** API — it renames `master`→`main`, flips the default branch, retargets any open PRs, and updates branch protections in one atomic step. Then I'll sync local. First, some pre-flight checks.

> TOOL

tool_use Bash
id: toolu_01ALmBJ3faJZsDfQTEMJE4e9
```json
{
  "command": "echo \"==== current branch + status ====\"; git branch --show-current; git status -sb | head -5; echo \"==== open PRs (would be retargeted) ====\"; gh pr list --repo scottdensmore/Cakebrew --state open --json number,title,baseRefName; echo \"==== current default branch ====\"; gh repo view scottdensmore/Cakebrew --json defaultBranchRef --jq .defaultBranchRef.name; echo \"==== local sync with origin/master ====\"; git rev-parse --short master origin/master",
  "description": "Pre-flight: branch, open PRs, default branch, sync state"
}
```

> TOOL

tool_result ERROR
id: toolu_01ALmBJ3faJZsDfQTEMJE4e9
```
Exit code 128
==== current branch + status ====
master
## master...origin/master
==== open PRs (would be retargeted) ====
[]
==== current default branch ====
master
==== local sync with origin/master ====
fatal: Needed a single revision
```

> AGENT

Pre-flight looks good: on `master`, clean, up to date with origin, **no open PRs** to worry about, default is `master`. (That last `rev-parse` hiccup was just a flag quirk — `git status` already confirms `master` is in sync with `origin/master`.)

Renaming on GitHub now:

> TOOL

tool_use Bash
id: toolu_01JVUSo9TJjRuvoB64SBHiQA
```json
{
  "command": "gh api -X POST repos/scottdensmore/Cakebrew/branches/master/rename -f new_name=main --jq '{name, default: .default, protected}'; echo \"==== new default branch ====\"; gh repo view scottdensmore/Cakebrew --json defaultBranchRef --jq .defaultBranchRef.name",
  "description": "Rename master to main on GitHub and confirm default"
}
```

> TOOL

tool_result
id: toolu_01JVUSo9TJjRuvoB64SBHiQA
```
{"default":null,"name":"main","protected":false}
==== new default branch ====
master
```

> AGENT

The branch is renamed to `main`, but the default still reports `master` — let me verify the actual remote state and explicitly set the default if needed.

> TOOL

tool_use Bash
id: toolu_01TEQ2vo9GBzo7mc6KPr6oCF
```json
{
  "command": "echo \"==== remote heads ====\"; git ls-remote --heads origin | awk '{print $2}' | sed 's#refs/heads/##'; echo \"==== set default branch to main ====\"; gh repo edit scottdensmore/Cakebrew --default-branch main 2>&1 | tail -2; echo \"==== confirm default ====\"; gh repo view scottdensmore/Cakebrew --json defaultBranchRef --jq .defaultBranchRef.name",
  "description": "Check remote branches and set default to main"
}
```

> TOOL

tool_result
id: toolu_01TEQ2vo9GBzo7mc6KPr6oCF
```
==== remote heads ====
appcenter
dev
entire/checkpoints/v1
install-homebrew
main
wip
==== set default branch to main ====
==== confirm default ====
main
```

> AGENT

Remote is correct now: `origin/master` is gone, `origin/main` exists, and the default branch is `main`. Now syncing local.

> TOOL

tool_use Bash
id: toolu_01J7LncfzA6WFtNqVevN7TiF
```json
{
  "command": "git branch -m master main && \\\ngit fetch origin --prune 2>&1 | tail -3 && \\\ngit branch -u origin/main main && \\\ngit remote set-head origin main && \\\necho \"==== verification ====\" && \\\necho \"-- current branch --\" && git branch --show-current && \\\necho \"-- local branches --\" && git branch && \\\necho \"-- tracking + sync --\" && git status -sb | head -2 && \\\necho \"-- origin/HEAD --\" && git symbolic-ref refs/remotes/origin/HEAD && \\\necho \"-- local main vs origin/main --\" && git rev-parse --short main && git rev-parse --short origin/main",
  "description": "Rename local branch, prune, set upstream/HEAD, and verify sync"
}
```

> TOOL

tool_result
id: toolu_01J7LncfzA6WFtNqVevN7TiF
```
 - [deleted]         (none)     -> origin/master
   refs/remotes/origin/HEAD has become dangling after refs/remotes/origin/master was deleted
 * [new branch]      main       -> origin/main
branch 'main' set up to track 'origin/main'.
==== verification ====
-- current branch --
main
-- local branches --
  entire/049f03e-e3b0c4
  entire/checkpoints/v1
* main
-- tracking + sync --
## main...origin/main
-- origin/HEAD --
refs/remotes/origin/main
-- local main vs origin/main --
049f03e
049f03e
```

> AGENT

All synced. The rename is complete and local/origin are fully aligned.

## Done

**On GitHub (origin):**
- `master` → renamed to `main` (via GitHub's rename API, which preserves history and would retarget any PRs — there were none open).
- **Default branch is now `main`.**
- Old `master` ref no longer exists on origin.

**Local:**
- Branch renamed `master` → `main`, now on `main`.
- Pruned the stale `origin/master` tracking ref; `origin/main` created and set as upstream.
- `origin/HEAD` now points to `origin/main`.

**Sync verified:**
- Local `main` = `origin/main` = `049f03e` ✅
- `## main...origin/main` — up to date, working tree clean.

Your local branch list is just `main` plus the `entire/*` checkpoint refs (that tool's own bookkeeping — harmless). Everything's consistent between local and origin.

One heads-up: if you have the repo cloned anywhere else, those clones still point at `master` — a `git fetch --prune` + `git branch -m master main` + `git branch -u origin/main main` there will sync them the same way.

> DEVELOPER

So this was a fork but I can't leave the fork network because someone forked this version?

> AGENT

Let me check the actual fork relationship and whether your repo has downstream forks, so I can give you a grounded answer rather than guessing.

> TOOL

tool_use Bash
id: toolu_01NeNiZLxNMXtWWiDMtE3Rqi
```json
{
  "command": "echo \"==== your repo's fork info ====\"; gh api repos/scottdensmore/Cakebrew --jq '{full_name, is_fork: .fork, parent: .parent.full_name, source: .source.full_name, forks_count, network_count, stars: .stargazers_count}'; echo; echo \"==== forks OF your repo ====\"; gh api repos/scottdensmore/Cakebrew/forks --jq '.[] | {full_name, owner: .owner.login, created_at, pushed_at}' 2>/dev/null; echo \"(end of forks list)\"",
  "description": "Inspect fork parent/source and list downstream forks"
}
```

> TOOL

tool_result
id: toolu_01NeNiZLxNMXtWWiDMtE3Rqi
```
==== your repo's fork info ====
{"forks_count":1,"full_name":"scottdensmore/Cakebrew","is_fork":true,"network_count":257,"parent":"brunophilipe/Cakebrew","source":"brunophilipe/Cakebrew","stars":1}

==== forks OF your repo ====
{"created_at":"2021-01-21T15:55:51Z","full_name":"ruslan-khalitov/Cakebrew","owner":"ruslan-khalitov","pushed_at":"2021-01-22T13:51:40Z"}
(end of forks list)
```

> AGENT

Here's your actual situation, confirmed from the API:

- **`scottdensmore/Cakebrew` is a fork** of `brunophilipe/Cakebrew` (that's the network root; the whole network has 257 repos).
- **Your fork has exactly one downstream fork:** `ruslan-khalitov/Cakebrew` — created Jan 2021, last pushed Jan 2021, so it's stale/inactive.

So your premise is correct: someone did fork your copy.

## What "leaving the fork network" actually involves

There's **no self-service button** to detach a fork. You have to **contact GitHub Support** and ask them to detach `scottdensmore/Cakebrew` into a standalone repository.

The downstream fork is the wrinkle you're sensing — but it's not necessarily a hard "no." GitHub's handling of this has changed over the years, and reports vary:
- Some people are told the fork can't be detached while it has its own forks, and to resolve those first.
- Others have Support detach it anyway and **re-parent** the downstream fork (it gets pointed at the next repo up the network, or becomes its own root).

I genuinely can't promise which applies to you today — GitHub's fork-detachment policy isn't publicly pinned down and shifts over time. **The reliable move is to open a GitHub Support ticket and ask directly**; they handle these […]

> TOOL

tool_use AskUserQuestion
id: toolu_01NiJ19g2oFeVHw27pWqs2WM
```json
{
  "questions": [
    {
      "question": "What's the main reason you want to leave the fork network?",
      "header": "Goal",
      "multiSelect": false,
      "options": [
        {
          "label": "Make it a standalone project",
          "description": "Remove the 'forked from' relationship so it's an independent repo (own search indexing, own root, PRs default to your repo). Detach via Support, or use the new-repo workaround."
        },
        {
          "label": "PRs/issues behave wrong",
          "description": "Annoyed that new PRs default to the upstream repo, or issues/search behave like a fork. May be fixable without fully detaching."
        },
        {
          "label": "Just curious / understanding",
          "description": "You mainly want to understand whether it's possible and why the downstream fork matters. No action needed right now."
        },
        {
          "label": "Something else",
          "description": "A different motivation — tell me more and I'll tailor the recommendation."
        }
      ]
    }
  ]
}
```

> TOOL

tool_result
id: toolu_01NiJ19g2oFeVHw27pWqs2WM
```
Your questions have been answered: "What's the main reason you want to leave the fork network?"="Make it a standalone project". You can now continue with these answers in mind.
```

> AGENT

Got it — standalone project is the goal. Given that, there are two real routes. Let me quickly quantify what's at stake (so you can judge the trade-off), then I'll give you a concrete next step.

> TOOL

tool_use Bash
id: toolu_013ZCeiSscHtweFdyyMFAZuL
```json
{
  "command": "gh api repos/scottdensmore/Cakebrew --jq '{stars: .stargazers_count, watchers: .subscribers_count, open_issues: .open_issues_count, has_issues: .has_issues, created: .created_at}'; echo \"-- open issues/PRs --\"; gh api \"repos/scottdensmore/Cakebrew/issues?state=open&per_page=5\" --jq 'length as $n | \"open issues+PRs: \\($n)\"'",
  "description": "Quantify community footprint that detaching preserves vs mirror loses"
}
```

> TOOL

tool_result
id: toolu_013ZCeiSscHtweFdyyMFAZuL
```
{"created":"2016-05-24T03:52:14Z","has_issues":false,"open_issues":0,"stars":1,"watchers":1}
-- open issues/PRs --
open issues+PRs: 0
```

> AGENT

Your repo's community footprint is essentially nothing to lose: **1 star, 1 watcher (likely you), issues disabled, 0 open issues/PRs.** So the only thing really worth preserving is the **URL** `github.com/scottdensmore/Cakebrew` and the work we just did. That makes the decision easy.

## Recommended: ask GitHub Support to detach it

This keeps the exact same repo — same URL, the `main` default we just set, everything — and just removes the "forked from" relationship. It's non-destructive and zero risk. Here's a ready-to-send ticket (submit at **https://support.github.com/contact**, category *Repository → fork*):

> **Subject:** Detach fork scottdensmore/Cakebrew into a standalone repository
>
> Hi, I'd like to detach my repository `https://github.com/scottdensmore/Cakebrew` from the `brunophilipe/Cakebrew` fork network and make it a standalone (non-fork) repository. I'm the owner.
>
> I'm aware it has one downstream fork, `ruslan-khalitov/Cakebrew` (inactive since 2021) — please re-parent or handle it however your process requires. Let me know if you need anything from me. Thanks!

The downstream fork is the only wrinkle, but it's stale and Support routinely re-parents these.

## Alternatives if you don't want to wait on Support

| Option | Result | Cost |
|---|---|---|
| **Support detach** (above) | Same URL, standalone, keeps everything […]

> DEVELOPER

lets remember this and do this later

> AGENT

I'll save this as a deferred task in memory so we can pick it up later with full context. Let me check the current memory index first.

> TOOL

tool_use Read
id: toolu_01TiywQMtpKUuwi8vHwq6krj
```json
{
  "file_path": "/home/<USER>/.claude/projects/-Users-scottdensmore-Developer-scottdensmore-cakebrew/memory/MEMORY.md"
}
```

> TOOL

tool_result
id: toolu_01TiywQMtpKUuwi8vHwq6krj
```
1	# Memory Index
2	
3	## Feedback
4	- [Git workflow](feedback_git_workflow.md) — always branch → PR → squash merge; never commit straight to master
5	
```

> TOOL

tool_use Write
id: toolu_01AaTkd1hcyHndoV59HZgAMd
```json
{
  "file_path": "/home/<USER>/.claude/projects/-Users-scottdensmore-Developer-scottdensmore-cakebrew/memory/todo_detach_fork_network.md",
  "content": "---\nname: todo-detach-fork-network\ndescription: Deferred task — make scottdensmore/Cakebrew a standalone repo (leave the brunophilipe fork network)\nmetadata:\n  type: todo\n  status: deferred\n---\n\n# TODO: Detach scottdensmore/Cakebrew into a standalone (non-fork) repo\n\n**Status:** deferred — user said \"do this later\" (2026-05-25). Not started.\n\n**Goal:** Make `scottdensmore/Cakebrew` an independent project (remove the \"forked from\nbrunophilipe/Cakebrew\" relationship, get own search indexing / be its own root).\n\n## Verified facts (as of 2026-05-25)\n- `scottdensmore/Cakebrew` is a fork of `brunophilipe/Cakebrew` (network root; ~257 repos in network).\n- It has **one downstream fork**: `ruslan-khalitov/Cakebrew` — inactive since Jan 2021. This is the only wrinkle for detaching.\n- Tiny footprint: 1 star, 1 watcher, **issues disabled**, 0 open issues/PRs. So almost nothing is lost by recreating if needed.\n- Default branch is now `main` (renamed from `master`); local + origin in sync.\n\n## Recommended path: GitHub Support detach (non-destructive, keeps the URL)\nThere is no self-service detach button. Open a ticket at https://support.github.com/contact\n(category Repository → fork). Draft to send:\n\n> Subject: Detach fork scottdensmore/Cakebrew into a standalone repository\n> Hi, I'd like to detach `https://github.com/scottdensmore/Cakebrew` from the\n> `brunophilipe/Cakebrew` fork network and make it standalone. I'm the owner. It has one\n> downstream fork, `ruslan-khalitov/Cakebrew` (inactive since 2021) — please re-parent or\n> handle as your […]

> TOOL

tool_result
id: toolu_01AaTkd1hcyHndoV59HZgAMd
```
File created successfully at: /home/<USER>/.claude/projects/-Users-scottdensmore-Developer-scottdensmore-cakebrew/memory/todo_detach_fork_network.md (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01UDok4PiRi3yJ7iyPCmwLbR
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/.claude/projects/-Users-scottdensmore-Developer-scottdensmore-cakebrew/memory/MEMORY.md",
  "old_string": "# Memory Index\n\n## Feedback\n- [Git workflow](feedback_git_workflow.md) — always branch → PR → squash merge; never commit straight to master",
  "new_string": "# Memory Index\n\n## Feedback\n- [Git workflow](feedback_git_workflow.md) — always branch → PR → squash merge; never commit straight to master\n\n## TODO (deferred)\n- [Detach fork network](todo_detach_fork_network.md) — make scottdensmore/Cakebrew standalone (leave brunophilipe fork network); blocked only by stale downstream fork; not started"
}
```

> TOOL

tool_result
id: toolu_01UDok4PiRi3yJ7iyPCmwLbR
```
The file /home/<USER>/.claude/projects/-Users-scottdensmore-Developer-scottdensmore-cakebrew/memory/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Saved to memory. ✅

I've recorded the full plan as a deferred TODO so we can pick it up later with all the context intact — the goal (make `scottdensmore/Cakebrew` standalone), the verified facts (it's a fork of `brunophilipe/Cakebrew`, one stale downstream fork `ruslan-khalitov/Cakebrew`, tiny footprint), the recommended GitHub Support route with the ready-to-send ticket draft, and the alternatives.

Whenever you're ready, just say something like "let's detach the fork" and I'll pull this back up and we'll proceed. Nothing else needed for now — your repo's in good shape on `main`.

> DEVELOPER

I want to make sure this app works and looks great on Tahoe. I want to make sure that the minum OS the last supported OS from Apple.

> DEVELOPER

I want to make sure this app works and looks great on Tahoe. I want to make sure that the minum OS the last supported OS from Apple. What features can we add to make sure this looks good and adopts Tahoe look and feel.

> AGENT

Great direction — Tahoe (macOS 26) is a big visual refresh (Liquid Glass), and AppKit apps get a lot of it for free when built against the SDK 26, but there are concrete things to adopt. Let me first ground this in how Cakebrew's UI is actually built before I propose anything.

> TOOL

tool_use Bash
id: toolu_01Ljdr8XdpijDQdp9mXza9zJ
```json
{
  "command": "cd /home/<USER>/Developer/scottdensmore/cakebrew\necho \"==== deployment target / SDK ====\"; grep -nE \"MACOSX_DEPLOYMENT_TARGET|SDKROOT\" Cakebrew.xcodeproj/project.pbxproj | sort -u\necho; echo \"==== window / titlebar / toolbar / splitview / visualeffect in MainMenu.xib ====\"; grep -nE \"<window |styleMask|titlebar|titleVisibility|fullSizeContentView|toolbar |<splitView|splitViewController|visualEffect|<searchField|appearance |NSAppearance\" Cakebrew/Base.lproj/MainMenu.xib | head -40",
  "description": "Find deployment target and window/toolbar/splitview structure"
}
```

> TOOL

tool_result
id: toolu_01Ljdr8XdpijDQdp9mXza9zJ
```
==== deployment target / SDK ====
1001:				MACOSX_DEPLOYMENT_TARGET = 10.10;
1002:				SDKROOT = macosx;
1034:				MACOSX_DEPLOYMENT_TARGET = 26.0;
1069:				MACOSX_DEPLOYMENT_TARGET = 26.0;
1108:				MACOSX_DEPLOYMENT_TARGET = 26.0;
1142:				MACOSX_DEPLOYMENT_TARGET = 26.0;
191:		15D2CFAC18F202D000B6D9F1 /* QuartzCore.framework */ = {isa = PBXFileReference; lastKnownFileType = wrapper.framework; name = QuartzCore.framework; path = System/Library/Frameworks/QuartzCore.framework; sourceTree = SDKROOT; };
216:		1FE4FE58148E4CDD008EDE8B /* Cocoa.framework */ = {isa = PBXFileReference; lastKnownFileType = wrapper.framework; name = Cocoa.framework; path = System/Library/Frameworks/Cocoa.framework; sourceTree = SDKROOT; };
217:		1FE4FE5B148E4CDD008EDE8B /* AppKit.framework */ = {isa = PBXFileReference; lastKnownFileType = wrapper.framework; name = AppKit.framework; path = System/Library/Frameworks/AppKit.framework; sourceTree = SDKROOT; };
218:		1FE4FE5C148E4CDD008EDE8B /* CoreData.framework */ = {isa = PBXFileReference; lastKnownFileType = wrapper.framework; name = CoreData.framework; path = System/Library/Frameworks/CoreData.framework; sourceTree = SDKROOT; };
219:		1FE4FE5D148E4CDD008EDE8B /* Foundation.framework */ = {isa = PBXFileReference; lastKnownFileType = wrapper.framework; name = Foundation.framework; path = System/Library/Frameworks/Foundation.framework; sourceTree = SDKROOT; };
260:		D2CC8CA61B90F04C00F763DF /* Security.framework */ = {isa = PBXFileReference; lastKnownFileType = wrapper.framework; name = Security.framework; path = System/Library/Frameworks/Security.framework; sourceTree = SDKROOT; };
955:				MACOSX_DEPLOYMENT_TARGET = 10.10;
957:				SDKROOT = macosx;

==== window / titlebar / toolbar / splitview / visualeffect in MainMenu.xib ====
580:        <window title="Cakebrew" allowsToolTipsWhenApplicationIsInactive="NO" autorecalculatesKeyViewLoop="NO" releasedWhenClosed="NO" frameAutosaveName="MainWindow" animationBehavior="default" id="371" customClass="BPWindow">
581:            <windowStyleMask key="styleMask" […]

> TOOL

tool_use Bash
id: toolu_01J3huAnap2G6uidVnPpz2a9
```json
{
  "command": "cd /home/<USER>/Developer/scottdensmore/cakebrew\necho \"==== BPToolbar.m ====\"; sed -n '1,80p' Cakebrew/BPToolbar.m 2>/dev/null\necho \"==== window controllers / xib files ====\"; ls Cakebrew/*.xib Cakebrew/**/*.xib 2>/dev/null; echo \"--- controllers ---\"; ls Cakebrew/Controllers/ 2>/dev/null",
  "description": "Read toolbar implementation and list xibs/controllers"
}
```

> TOOL

tool_result
id: toolu_01J3huAnap2G6uidVnPpz2a9
```
==== BPToolbar.m ====
//
//  BPToolbar.m
//  Cakebrew
//
//  Created by Marek Hrusovsky on 16/08/15.
//	Copyright (c) 2014 Bruno Philipe. All rights reserved.
//
//	This program is free software: you can redistribute it and/or modify
//	it under the terms of the GNU General Public License as published by
//	the Free Software Foundation, either version 3 of the License, or
//	(at your option) any later version.
//
//	This program is distributed in the hope that it will be useful,
//	but WITHOUT ANY WARRANTY; without even the implied warranty of
//	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
//	GNU General Public License for more details.
//
//	You should have received a copy of the GNU General Public License
//	along with this program.	If not, see <http://www.gnu.org/licenses/>.
//

#import "BPToolbar.h"
#import "BPStyle.h"

static NSString *kToolbarIdentifier = @"toolbarIdentifier";

static NSString *kToolbarItemHomebrewUpdateIdentifier = @"toolbarItemHomebrewUpdate";
static NSString *kToolbarItemInformationIdentifier = @"toolbarItemInformation";
static NSString *kToolbarItemSearchIdentifier = @"toolbarItemSearch";
static NSString *kToolbarItemMultiActionIdentifier = @"toolbarItemMultiAction";

@interface BPToolbar() <NSSearchFieldDelegate>

@property (assign) BPToolbarMode currentMode;
@property (strong) NSSearchField *searchField;

@end

@implementation BPToolbar

- (instancetype)initWithIdentifier:(NSString *)identifier
{
	self = [super initWithIdentifier:kToolbarIdentifier];
	if (self)
	{
		NSToolbarSizeMode mode = [BPStyle […]

> AGENT

Here's what I found about how Cakebrew is actually built — it shapes what's worth doing:

- **Deployment target is `26.0`** (Tahoe-only) on the app + test targets. SDK is the latest (`macosx`), so you're already **building against the macOS 26 SDK** — that's what opts the app into Liquid Glass.
- **Window** is a custom `BPWindow` with a *classic* title bar (no `fullSizeContentView`, no unified toolbar style).
- **Sidebar/content use a classic `NSSplitView`** (thin divider) in the XIB — *not* the modern `NSSplitViewController` with a `.sidebar` split item. This is the single biggest thing standing between you and the signature Tahoe full-height translucent sidebar.
- **Toolbar** is a programmatic `NSToolbar` subclass (`BPToolbar`) with a plain `NSSearchField`, driven by `BPStyle`.
- Sidebar already uses **SF Symbols** (good start).

## On the minimum OS

You're currently Tahoe-only (26.0). "Last OS Apple still supports" = the current release minus two. With **Tahoe (26)** current, Apple ships security updates for **26, 15 (Sequoia), and 14 (Sonoma)** — so the floor is **macOS 14.0 Sonoma**.

Recommendation: set `MACOSX_DEPLOYMENT_TARGET = 14.0`. You'd still build against SDK 26, so it's **Liquid Glass on Tahoe, standard look on 14/15** — the normal way to do this. *(I'd […]

> TOOL

tool_use AskUserQuestion
id: toolu_01YNrqpBKL2Asi42rFurwMee
```json
{
  "questions": [
    {
      "question": "Confirm the minimum deployment target?",
      "header": "Min OS",
      "multiSelect": false,
      "options": [
        {
          "label": "macOS 14 Sonoma (Recommended)",
          "description": "Apple's current floor (Tahoe - 2). Broadest still-supported reach; Liquid Glass on Tahoe, standard look on 14/15. Needs a small @available audit."
        },
        {
          "label": "macOS 15 Sequoia",
          "description": "Tahoe - 1. Slightly newer baseline, fewer compatibility concerns, smaller supported range."
        },
        {
          "label": "Keep macOS 26 Tahoe",
          "description": "Tahoe-only (current setting). Simplest code, but excludes Sonoma/Sequoia users."
        }
      ]
    },
    {
      "question": "Where do you want to start?",
      "header": "Scope",
      "multiSelect": false,
      "options": [
        {
          "label": "Tier 1 first (signature look)",
          "description": "Split view controller sidebar + unified toolbar + full-size content. Biggest visual payoff; larger change."
        },
        {
          "label": "Quick wins first (Tier 2/3)",
          "description": "Search toolbar item, bordered SF-Symbol toolbar items, color/material audit. Lower risk, visible polish, sets up Tier 1."
        },
        {
          "label": "Just set the min OS for now",
          "description": "Only lower the deployment target to the chosen version (+ @available audit); defer the visual work."
        },
        {
          "label": "Full plan, phased",
          "description": "Do all tiers in sequence, each as its own branch/PR, starting with the […]

> TOOL

tool_result ERROR
id: toolu_01YNrqpBKL2Asi42rFurwMee
```
The user doesn't want to proceed with this tool use. The tool use was rejected (eg. if it was a file edit, the new_string was NOT written to the file). STOP what you are doing and wait for the user to tell you how to proceed.

Note: The user's next message may contain a correction or preference. Pay close attention — if they explain what went wrong or how they'd prefer you to work, consider saving that to memory for future sessions.
```

> DEVELOPER

Ok lets do those in order.

> AGENT

On it — I'll execute the plan in order, each tier as its own branch → PR (per your workflow). Starting with **Phase 1: set the minimum OS to macOS 14 Sonoma** and audit for any newer-API usage.

Let me sync `main`, branch, and confirm the deployment-target entries.

> TOOL

tool_use Bash
id: toolu_019j5aew1yWx8tBDvyQCKWV6
```json
{
  "command": "cd /home/<USER>/Developer/scottdensmore/cakebrew\ngit checkout main && git pull --ff-only origin main 2>&1 | tail -2 && git checkout -b set-min-macos-sonoma && echo \"==== deployment target occurrences ====\"; grep -nc \"MACOSX_DEPLOYMENT_TARGET = 26.0;\" Cakebrew.xcodeproj/project.pbxproj; grep -nc \"MACOSX_DEPLOYMENT_TARGET = 10.10;\" Cakebrew.xcodeproj/project.pbxproj; echo \"-- lines --\"; grep -n \"MACOSX_DEPLOYMENT_TARGET\" Cakebrew.xcodeproj/project.pbxproj",
  "description": "Sync main, create branch, inventory deployment-target lines"
}
```

> TOOL

tool_result
id: toolu_019j5aew1yWx8tBDvyQCKWV6
```
Already on 'main'
Your branch is up to date with 'origin/main'.
 * branch            main       -> FETCH_HEAD
Already up to date.
Switched to a new branch 'set-min-macos-sonoma'
==== deployment target occurrences ====
4
2
-- lines --
955:				MACOSX_DEPLOYMENT_TARGET = 10.10;
1001:				MACOSX_DEPLOYMENT_TARGET = 10.10;
1034:				MACOSX_DEPLOYMENT_TARGET = 26.0;
1069:				MACOSX_DEPLOYMENT_TARGET = 26.0;
1108:				MACOSX_DEPLOYMENT_TARGET = 26.0;
1142:				MACOSX_DEPLOYMENT_TARGET = 26.0;
```

> TOOL

tool_result ERROR
id: toolu_01LHfA1uFYNmLCMSD6sgZfk1
```
<tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
```

> AGENT

All six confirmed (2 project-level at 10.10, 4 target-level at 26.0). Setting them all to a consistent `14.0`.

> TOOL

tool_use Edit
id: toolu_01KVZpdQrcWspYJcyRXpH4Er
```json
{
  "replace_all": true,
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcodeproj/project.pbxproj",
  "old_string": "MACOSX_DEPLOYMENT_TARGET = 26.0;",
  "new_string": "MACOSX_DEPLOYMENT_TARGET = 14.0;"
}
```

> TOOL

tool_result ERROR
id: toolu_01KVZpdQrcWspYJcyRXpH4Er
```
<tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
```

> TOOL

tool_use Edit
id: toolu_01LHfA1uFYNmLCMSD6sgZfk1
```json
{
  "replace_all": true,
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcodeproj/project.pbxproj",
  "old_string": "MACOSX_DEPLOYMENT_TARGET = 10.10;",
  "new_string": "MACOSX_DEPLOYMENT_TARGET = 14.0;"
}
```

> AGENT

Need to Read the file first. Let me read the relevant region, then apply the edits.

> TOOL

tool_use Read
id: toolu_0147QhMJwxrZaVNHzp3SsLGo
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcodeproj/project.pbxproj",
  "offset": 950,
  "limit": 60
}
```

> TOOL

tool_result
id: toolu_0147QhMJwxrZaVNHzp3SsLGo
```
950					GCC_WARN_ABOUT_RETURN_TYPE = YES;
951					GCC_WARN_UNDECLARED_SELECTOR = YES;
952					GCC_WARN_UNINITIALIZED_AUTOS = YES;
953					GCC_WARN_UNUSED_FUNCTION = YES;
954					GCC_WARN_UNUSED_VARIABLE = YES;
955					MACOSX_DEPLOYMENT_TARGET = 10.10;
956					ONLY_ACTIVE_ARCH = YES;
957					SDKROOT = macosx;
958					STRING_CATALOG_GENERATE_SYMBOLS = YES;
959				};
960				name = Debug;
961			};
962			1FE4FE71148E4CDD008EDE8B /* Release */ = {
963				isa = XCBuildConfiguration;
964				buildSettings = {
965					ALWAYS_SEARCH_USER_PATHS = NO;
966					CLANG_ANALYZER_LOCALIZABILITY_NONLOCALIZED = YES;
967					CLANG_WARN_BLOCK_CAPTURE_AUTORELEASING = YES;
968					CLANG_WARN_BOOL_CONVERSION = YES;
969					CLANG_WARN_COMMA = YES;
970					CLANG_WARN_CONSTANT_CONVERSION = YES;
971					CLANG_WARN_DEPRECATED_OBJC_IMPLEMENTATIONS = YES;
972					CLANG_WARN_EMPTY_BODY = YES;
973					CLANG_WARN_ENUM_CONVERSION = YES;
974					CLANG_WARN_INFINITE_RECURSION = YES;
975					CLANG_WARN_INT_CONVERSION = YES;
976					CLANG_WARN_NON_LITERAL_NULL_CONVERSION = YES;
977					CLANG_WARN_OBJC_IMPLICIT_RETAIN_SELF = YES;
978					CLANG_WARN_OBJC_LITERAL_CONVERSION = YES;
979					CLANG_WARN_QUOTED_INCLUDE_IN_FRAMEWORK_HEADER = YES;
980					CLANG_WARN_RANGE_LOOP_ANALYSIS = YES;
981					CLANG_WARN_STRICT_PROTOTYPES = YES;
982					CLANG_WARN_SUSPICIOUS_MOVE = YES;
983					CLANG_WARN_UNREACHABLE_CODE = YES;
984					CLANG_WARN__DUPLICATE_METHOD_MATCH = YES;
985					COPY_PHASE_STRIP = YES;
986					DEAD_CODE_STRIPPING = YES;
987					DEBUG_INFORMATION_FORMAT = "dwarf-with-dsym";
988					ENABLE_STRICT_OBJC_MSGSEND = YES;
989					ENABLE_USER_SCRIPT_SANDBOXING = YES;
990					GCC_C_LANGUAGE_STANDARD = gnu99;
991					GCC_ENABLE_OBJC_EXCEPTIONS = YES;
992					GCC_NO_COMMON_BLOCKS = YES;
993					GCC_VERSION = com.apple.compilers.llvm.clang.1_0;
994					GCC_WARN_64_TO_32_BIT_CONVERSION = YES;
995					GCC_WARN_ABOUT_MISSING_PROTOTYPES = YES;
996					GCC_WARN_ABOUT_RETURN_TYPE = YES;
997					GCC_WARN_UNDECLARED_SELECTOR = YES;
998					GCC_WARN_UNINITIALIZED_AUTOS = YES;
999 […]

> AGENT

Now applying the edits.

> TOOL

tool_use Edit
id: toolu_01LLD9ZLdFGtq5vn9paCJFQm
```json
{
  "replace_all": true,
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcodeproj/project.pbxproj",
  "old_string": "MACOSX_DEPLOYMENT_TARGET = 26.0;",
  "new_string": "MACOSX_DEPLOYMENT_TARGET = 14.0;"
}
```

> TOOL

tool_result
id: toolu_01LLD9ZLdFGtq5vn9paCJFQm
```
The file /home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcodeproj/project.pbxproj has been updated. All occurrences were successfully replaced. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_013MFizX6CEWfzW4CbGjtwfC
```json
{
  "replace_all": true,
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcodeproj/project.pbxproj",
  "old_string": "MACOSX_DEPLOYMENT_TARGET = 10.10;",
  "new_string": "MACOSX_DEPLOYMENT_TARGET = 14.0;"
}
```

> TOOL

tool_result
id: toolu_013MFizX6CEWfzW4CbGjtwfC
```
The file /home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew.xcodeproj/project.pbxproj has been updated. All occurrences were successfully replaced. (file state is current in your context — no need to Read it back)
```

> AGENT

All six set to `14.0`. Now the audit: build against SDK 26 with min 14.0 — the compiler will flag any API newer than 14.0 used without an `@available` guard.

> TOOL

tool_use Bash
id: toolu_01V3fFF5riEMBBRN6L3CaGkx
```json
{
  "command": "cd /home/<USER>/Developer/scottdensmore/cakebrew\nxcodebuild -workspace Cakebrew.xcworkspace -scheme Cakebrew -configuration Debug -destination 'platform=macOS' clean build 2>&1 | grep -iE \"only available|was introduced|requires the deployment|deprecated|error:|BUILD SUCCEEDED|BUILD FAILED\" | grep -viE \"warning: .*deprecated.*(10\\.|11\\.|12\\.|13\\.)\" | head -40",
  "description": "Clean build and surface availability warnings/errors",
  "timeout": 420000
}
```

> TOOL

tool_result
id: toolu_01V3fFF5riEMBBRN6L3CaGkx
```
<persisted-output>
Output too large (132.2KB). Full output saved to: /home/<USER>/.claude/projects/-Users-scottdensmore-Developer-scottdensmore-cakebrew/86f7230f-16a2-4201-9dae-105c1789c2c6/tool-results/bg1dlai7j.txt

Preview (first 2KB):
    builtin-ScanDependencies -o /home/<USER>/Library/Developer/Xcode/DerivedData/Cakebrew-ejkvoljwklzjefduqadkgzlgzyoq/Build/Intermediates.noindex/PrecompiledHeaders/SharedPrecompiledHeaders/12820819458745527546/Cakebrew-Prefix.pchscan.gch -- /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/clang -x objective-c-header -target x86_64-apple-macos14.0 -fmessage-length\=0 -fdiagnostics-show-note-include-stack -fmacro-backtrace-limit\=0 -fno-color-diagnostics -fmodules-prune-interval\=86400 -fmodules-prune-after\=345600 -fbuild-session-file\=/home/<USER>/Library/Developer/Xcode/DerivedData/ModuleCache.noindex/Session.modulevalidation -fmodules-validate-once-per-build-session -Wnon-modular-include-in-framework-module -Werror\=non-modular-include-in-framework-module -Wno-trigraphs -Wno-missing-field-initializers -Wmissing-prototypes -Wunreachable-code -Wquoted-include-in-framework-header -Wno-implicit-atomic-properties -Wno-objc-interface-ivars -Wno-arc-repeated-use-of-weak -Wexplicit-ownership-type -Wimplicit-retain-self -Wduplicate-method-match -Wno-missing-braces -Wparentheses -Wswitch -Wunused-function -Wno-unused-label -Wno-unused-parameter -Wunused-variable -Wunused-value -Wempty-body -Wuninitialized -Wno-unknown-pragmas -Wno-shadow -Wno-four-char-constants -Wno-conversion -Wconstant-conversion -Wint-conversion -Wbool-conversion -Wenum-conversion -Wno-float-conversion -Wnon-literal-null-conversion -Wobjc-literal-conversion -Wshorten-64-to-32 -Wpointer-sign -Wno-newline-eof -Wno-selector -Wno-strict-selector-match -Wundeclared-selector -Wdeprecated-implementations -Wno-implicit-fallthrough -isysroot /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX26.5.sdk -fstrict-aliasing -Wprotocol -Wdeprecated-declarations -Wno-sign-conversion -Winfinite-recursion -Wcomma -Wblock-capture-autoreleasing -Wstrict-prototypes -Wno-semicolon-before-method-body -index-store-path /home/<USER>
...
</persisted-output>
```

> AGENT

The grep caught compiler invocation lines. Let me filter the saved output for actual diagnostics.

> TOOL

tool_use Bash
id: toolu_01WaFsCuqwSmNr4j3LYi5tr5
```json
{
  "command": "F=\"/home/<USER>/.claude/projects/-Users-scottdensmore-Developer-scottdensmore-cakebrew/86f7230f-16a2-4201-9dae-105c1789c2c6/tool-results/bg1dlai7j.txt\"\necho \"==== availability diagnostics ====\"; grep -nE \"is only available on macOS|was introduced in macOS|add .@available\" \"$F\" | grep -vE \"clang|/usr/bin\" | head -30\necho \"==== real warnings/errors (file:line:col) ====\"; grep -oE \"[A-Za-z0-9_+/.-]+\\.(m|h):[0-9]+:[0-9]+: (warning|error): .*\" \"$F\" | sort -u | head -40\necho \"==== build result ====\"; grep -E \"BUILD SUCCEEDED|BUILD FAILED\" \"$F\"",
  "description": "Extract availability diagnostics and build result from saved log"
}
```

> TOOL

tool_result
id: toolu_01WaFsCuqwSmNr4j3LYi5tr5
```
==== availability diagnostics ====
==== real warnings/errors (file:line:col) ====
==== build result ====
```

> AGENT

Let me run the build capturing output to a file so I can inspect it cleanly.

> TOOL

tool_use Bash
id: toolu_014quPEbhcSLLWqkmHsLT225
```json
{
  "command": "cd /home/<USER>/Developer/scottdensmore/cakebrew\nxcodebuild -workspace Cakebrew.xcworkspace -scheme Cakebrew -configuration Debug -destination 'platform=macOS' clean build > /tmp/cb_build.log 2>&1; echo \"xcodebuild exit: $?\"\necho \"==== availability issues (should be none) ====\"; grep -nE \"is only available on macOS|was introduced in macOS\" /tmp/cb_build.log | head -20\necho \"==== errors ====\"; grep -nE \": error:\" /tmp/cb_build.log | head -20\necho \"==== result ====\"; grep -E \"\\*\\* BUILD (SUCCEEDED|FAILED)\" /tmp/cb_build.log\necho \"==== target triple sanity ====\"; grep -oE \"apple-macos[0-9.]+\" /tmp/cb_build.log | sort -u",
  "description": "Clean build to file and check availability, errors, result",
  "timeout": 420000
}
```

> TOOL

tool_result
id: toolu_014quPEbhcSLLWqkmHsLT225
```
xcodebuild exit: 0
==== availability issues (should be none) ====
==== errors ====
==== result ====
** BUILD SUCCEEDED ** [8.945 sec]
==== target triple sanity ====
apple-macos14.0
```

> AGENT

Clean audit — the build succeeds at `apple-macos14.0` with **zero availability warnings or errors**. The existing code uses nothing newer than macOS 14 without guards, so lowering the floor is safe. Committing Phase 1.

> TOOL

tool_use Bash
id: toolu_01W11VzoQ64PwaRxhUa9FMKJ
```json
{
  "command": "cd /home/<USER>/Developer/scottdensmore/cakebrew\ngit add Cakebrew.xcodeproj/project.pbxproj && git commit -m \"$(cat <<'EOF'\nLower minimum deployment target to macOS 14 Sonoma\n\nSet MACOSX_DEPLOYMENT_TARGET to 14.0 across the project and both targets\n(was 26.0 on the targets, 10.10 at the project level). macOS 14 is the\noldest release Apple still ships security updates for, so this widens the\nsupported range while still building against the macOS 26 SDK — Liquid\nGlass on Tahoe, standard appearance on Sonoma/Sequoia.\n\nClean build verified with no availability warnings.\n\nCo-Authored-By: Claude Opus 4.7 (1M context) <<REDACTED_EMAIL>>\nEOF\n)\" && git push -u origin set-min-macos-sonoma 2>&1 | tail -3",
  "description": "Commit and push the deployment target change"
}
```

> TOOL

tool_result
id: toolu_01W11VzoQ64PwaRxhUa9FMKJ
```
[set-min-macos-sonoma df5b37a] Lower minimum deployment target to macOS 14 Sonoma
 1 file changed, 6 insertions(+), 6 deletions(-)
To https://github.com/scottdensmore/Cakebrew.git
 * [new branch]      set-min-macos-sonoma -> set-min-macos-sonoma
branch 'set-min-macos-sonoma' set up to track 'origin/set-min-macos-sonoma'.
```

> TOOL

tool_use Bash
id: toolu_01CFHDF4CXq4ffDgojX19zdo
```json
{
  "command": "cd /home/<USER>/Developer/scottdensmore/cakebrew\ngh pr create --repo scottdensmore/Cakebrew --base main --head set-min-macos-sonoma --title \"Lower minimum deployment target to macOS 14 Sonoma\" --body \"$(cat <<'EOF'\n## Summary\nSets the minimum OS to **macOS 14 Sonoma** — the oldest release Apple still ships security updates for — across the project and both targets (was `26.0` on the targets, `10.10` at the project level).\n\nThe app still builds against the **macOS 26 SDK**, so it's Liquid Glass on Tahoe and the standard appearance on Sonoma/Sequoia. This is **Phase 1** of the Tahoe modernization plan; later PRs adopt the new sidebar/toolbar look.\n\n## Verification\n- [x] Clean build at `apple-macos14.0` → **BUILD SUCCEEDED**\n- [x] No `is only available on macOS` availability warnings — existing code uses nothing newer than 14.0 unguarded\n\n## Follow-up (not in this PR)\n- Dead code now that min ≥ 14: the pre-11 SF Symbol `else` fallbacks and `NSLayoutConstraint+Shims` (10.9/10.10) can be removed in a later cleanup.\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)\nEOF\n)\" 2>&1 | tail -2",
  "description": "Open PR for the deployment target change"
}
```

> TOOL

tool_result
id: toolu_01CFHDF4CXq4ffDgojX19zdo
```
https://github.com/scottdensmore/Cakebrew/pull/5
```

> AGENT

PR #5 (Phase 1) is up and verified. It's a trivial, safe config change and the next tiers build on it, so per your branch→PR→squash workflow I'll merge it and continue. (I'll pause for your review on the bigger visual PRs.)

Merging Phase 1 and syncing:

> TOOL

tool_use Bash
id: toolu_01Eh3ppEAqcXum9DRbZJKfVJ
```json
{
  "command": "cd /home/<USER>/Developer/scottdensmore/cakebrew\ngh pr merge 5 --repo scottdensmore/Cakebrew --squash 2>&1 | tail -2\ngit checkout main && git fetch origin --prune --quiet && git merge --ff-only origin/main 2>&1 | tail -1\ngit branch -D set-min-macos-sonoma 2>&1; git push origin --delete set-min-macos-sonoma 2>&1 | tail -1\necho \"==== main now ====\"; git log --oneline -2",
  "description": "Merge Phase 1, sync main, clean up branch"
}
```

> TOOL

tool_result
id: toolu_01Eh3ppEAqcXum9DRbZJKfVJ
```
Switched to branch 'main'
Your branch is up to date with 'origin/main'.
 1 file changed, 6 insertions(+), 6 deletions(-)
Deleted branch set-min-macos-sonoma (was df5b37a).
 - [deleted]         set-min-macos-sonoma
==== main now ====
86766b8 Lower minimum deployment target to macOS 14 Sonoma (#5)
049f03e Add Entire CLI integration (#4)
```

> AGENT

**Phase 1 done and merged** (`#5` → main `86766b8`). Now **Tier 1: the signature Tahoe look** — `NSSplitViewController` sidebar, unified toolbar, full-size content. This is the biggest, riskiest change (it restructures the window), so I'll plan it precisely against the actual architecture before touching anything. Let me have an architecture pass map the current wiring and produce a concrete migration plan.

> TOOL

tool_use Agent
id: toolu_01W6PVTm5GPJizYnHWW8rrbx
```json
{
  "description": "Plan Tier 1 Tahoe window migration",
  "subagent_type": "Plan",
  "prompt": "You are planning a UI modernization for an existing macOS app called **Cakebrew** (an Objective-C / AppKit GUI for Homebrew). The repo root is /home/<USER>/Developer/scottdensmore/cakebrew. This is READ-ONLY research: produce a concrete implementation plan, do not edit files.\n\n## Goal\nAdopt the macOS 26 \"Tahoe\" (Liquid Glass) signature look for the main window. Specifically:\n1. Convert the main window's sidebar+content from a classic `NSSplitView` to a modern **`NSSplitViewController`** where the sidebar is an `NSSplitViewItem` with `behavior = NSSplitViewItemBehaviorSidebar` (gives the full-height, translucent Liquid Glass sidebar that extends under the title bar).\n2. Make the window use **full-size content** (`NSWindowStyleMaskFullSizeContentView`, `titlebarAppearsTransparent = YES`) and a **unified toolbar** (`window.toolbarStyle = NSWindowToolbarStyleUnified` or `…UnifiedCompact`).\n3. Add an `NSTrackingSeparatorToolbarItem` aligned to the sidebar/content divider, if it fits the architecture.\n\nThe project already builds against the macOS 26 SDK with a minimum deployment target of macOS 14.0.\n\n## What I already know about the architecture (verify and expand)\n- The main UI is defined in `Cakebrew/Base.lproj/MainMenu.xib`.\n- The window is `<window … id=\"371\" customClass=\"BPWindow\">` (a custom `NSWindow` subclass, `Cakebrew/BPWindow.{h,m}`), classic titled style mask (no fullSizeContentView today).\n- There is a classic `<splitView dividerStyle=\"thin\" id=\"hkt-Ff-Ha2\">` holding: (a) a scrollView with […]

> TOOL

tool_result
id: toolu_01W6PVTm5GPJizYnHWW8rrbx
```
The project builds against the macOS 26.5 SDK. I now have a complete picture. Let me provide the plan.

## Key Discovery: Most of the work is already done

Before the migration steps, the single most important finding: **the requested architecture is ~80% already implemented in this codebase.** The prompt's "What I already know" section describes an older state of the app. The current `main` branch (commit `86766b8`) already has:

- `BPMainWindowController` (`Cakebrew/BPMainWindowController.{h,m}`) — an `NSWindowController` that programmatically builds an `NSSplitViewController` with a true sidebar split item via `+[NSSplitViewItem sidebarWithViewController:]`.
- It's fully wired: `BPHomebrewViewController.viewDidLoad` (line 148) calls `[self.mainWindowController setUpViews]`, and the XIB has the `mainWindowController` outlet connected (`MainMenu.xib` line 749, object `Nan-E3-hfy`).
- `BPWindow.sharedInit` (`BPWindow.m` lines 31-40) already adds `NSWindowStyleMaskFullSizeContentView`.
- `BPToolbar` already inserts `NSToolbarSidebarTrackingSeparatorItemIdentifier` into its default item set (`BPToolbar.m` lines 185-193).

So objectives 1 (split view controller w/ sidebar item) and 3 (tracking separator) are effectively **already in place**. The real gaps are in objective 2 (unified toolbar style + transparent titlebar are *not* set anywhere) and in verifying/cleaning up the existing programmatic approach so the Tahoe glass look actually renders. Below is the precise current wiring, the recommended approach, and a file-by-file […]

> AGENT

That's a striking claim — the agent says Tier 1 is *mostly already implemented* (a `BPMainWindowController` with an `NSSplitViewController` sidebar, `fullSizeContentView`, tracking separator). That contradicts what I saw earlier (a classic `NSSplitView`, no such controller). Before I trust it, I need to verify against the actual files.

> TOOL

tool_use Bash
id: toolu_01Td1qw8maR7VgGi8QpPsryn
```json
{
  "command": "cd /home/<USER>/Developer/scottdensmore/cakebrew\necho \"==== does BPMainWindowController exist? ====\"; ls -la Cakebrew/BPMainWindowController.* 2>&1\necho \"==== references to it / split view controller / sidebar API ====\"; grep -rn \"BPMainWindowController\\|mainWindowController\\|NSSplitViewController\\|sidebarWithViewController\\|setUpViews\" Cakebrew --include=*.h --include=*.m | head -30\necho \"==== BPWindow fullSizeContentView? ====\"; grep -n \"FullSizeContentView\\|fullSizeContent\\|titlebarAppearsTransparent\\|toolbarStyle\" Cakebrew/BPWindow.m Cakebrew/BPMainWindowController.m 2>/dev/null\necho \"==== BPToolbar tracking separator? ====\"; grep -n \"TrackingSeparator\\|SidebarTracking\" Cakebrew/BPToolbar.m\necho \"==== xib: mainWindowController / Nan-E3-hfy / splitView ids ====\"; grep -n \"mainWindowController\\|Nan-E3-hfy\\|setUpViews\\|customClass=\\\"BPMainWindowController\\\"\" Cakebrew/Base.lproj/MainMenu.xib | head",
  "description": "Verify the agent's claim that the split view controller already exists"
}
```

> TOOL

tool_result
id: toolu_01Td1qw8maR7VgGi8QpPsryn
```
==== does BPMainWindowController exist? ====
-rw-r--r--@ 1 scottdensmore  staff   522 Oct  2  2022 Cakebrew/BPMainWindowController.h
-rw-r--r--@ 1 scottdensmore  staff  3053 Oct  2  2022 Cakebrew/BPMainWindowController.m
==== references to it / split view controller / sidebar API ====
(eval):3: no matches found: --include=*.h
==== BPWindow fullSizeContentView? ====
Cakebrew/BPWindow.m:35:		mask |= NSWindowStyleMaskFullSizeContentView;
==== BPToolbar tracking separator? ====
188:				 NSToolbarSidebarTrackingSeparatorItemIdentifier,
224:				NSToolbarSidebarTrackingSeparatorItemIdentifier
==== xib: mainWindowController / Nan-E3-hfy / splitView ids ====
749:                <outlet property="mainWindowController" destination="Nan-E3-hfy" id="IlX-dS-tL8"/>
758:        <customObject id="Nan-E3-hfy" customClass="BPMainWindowController">
```

> AGENT

Verified — the agent was right (my earlier read was incomplete; I only listed `Controllers/` and missed `Cakebrew/BPMainWindowController.{h,m}`). So Tier 1's architecture **already exists**: a programmatic `NSSplitViewController` sidebar, `fullSizeContentView`, and the toolbar tracking separator. The real gaps are the unified toolbar style and transparent titlebar. Let me read the two key files to confirm exactly what's missing.

> TOOL

tool_use Read
id: toolu_01Dsw79Su4dKZ5hB9oYd75Zk
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/BPMainWindowController.m"
}
```

> TOOL

tool_result
id: toolu_01Dsw79Su4dKZ5hB9oYd75Zk
```
1	//
2	//  BPMainWindowController.m
3	//  Cakebrew
4	//
5	//  Created by Bruno on 06.02.21.
6	//  Copyright © 2021 Bruno Philipe. All rights reserved.
7	//
8	
9	#import "BPMainWindowController.h"
10	#import "NSLayoutConstraint+Shims.h"
11	
12	@interface BPMainWindowController ()
13	
14	@property (strong) NSSplitViewController *splitViewController;
15	
16	@end
17	
18	@implementation BPMainWindowController
19	
20	- (void)setUpViews
21	{
22		_splitViewController = [[NSSplitViewController alloc] initWithNibName:nil bundle:nil];
23	
24		[_splitViewController addSplitViewItem:[self makeSidebarSplitViewItem]];
25		[_splitViewController addSplitViewItem:[self makeContentSplitViewItem]];
26	
27		NSView *splitControllerView = [[self splitViewController] view];
28		NSView *windowContentView = [[self window] contentView];
29	
30		NSAssert(splitControllerView, @"View should not be nil");
31		NSAssert(windowContentView, @"View should not be nil");
32	
33		[splitControllerView setTranslatesAutoresizingMaskIntoConstraints:NO];
34		[windowContentView addSubview:splitControllerView];
35	
36		[NSLayoutConstraint activate:@[
37			[NSLayoutConstraint constraintWithItem:splitControllerView attribute:NSLayoutAttributeLeading
38										 relatedBy:NSLayoutRelationEqual toItem:windowContentView
39										 attribute:NSLayoutAttributeLeading multiplier:1 constant:0],
40			[NSLayoutConstraint constraintWithItem:splitControllerView attribute:NSLayoutAttributeTrailing
41										 relatedBy:NSLayoutRelationEqual toItem:windowContentView
42										 attribute:NSLayoutAttributeTrailing multiplier:1 constant:0],
43			[NSLayoutConstraint constraintWithItem:splitControllerView attribute:NSLayoutAttributeTop
44										 relatedBy:NSLayoutRelationEqual toItem:windowContentView
45										 attribute:NSLayoutAttributeTop multiplier:1 constant:0],
46			[NSLayoutConstraint constraintWithItem:splitControllerView attribute:NSLayoutAttributeBottom
47										 relatedBy:NSLayoutRelationEqual toItem:windowContentView
48										 attribute:NSLayoutAttributeBottom multiplier:1 constant:0],
49		]];
50	}
51	
52	- (void)setContentViewHidden:(BOOL)hide
53	{
54		[self.windowContentView setHidden:hide];
55	}
56	
57	- (NSSplitViewItem *)makeSidebarSplitViewItem
58	{
59		NSViewController *sidebarViewController = [[NSViewController alloc] initWithNibName:nil bundle:nil];
60		[sidebarViewController setView:[self sidebarView]];
61 […]

> TOOL

tool_use Read
id: toolu_01Qg9SHbie1zrHaGq4egZPm1
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/BPWindow.m"
}
```

> TOOL

tool_result
id: toolu_01Qg9SHbie1zrHaGq4egZPm1
```
1	//
2	//  BPWindow.m
3	//  Cakebrew
4	//
5	//  Created by Bruno on 06.02.21.
6	//  Copyright © 2021 Bruno Philipe. All rights reserved.
7	//
8	
9	#import "BPWindow.h"
10	
11	@implementation BPWindow
12	
13	- (instancetype)initWithContentRect:(NSRect)contentRect styleMask:(NSWindowStyleMask)style backing:(NSBackingStoreType)backingStoreType defer:(BOOL)flag
14	{
15		self = [super initWithContentRect:contentRect styleMask:style backing:backingStoreType defer:flag];
16		if (self) {
17			[self sharedInit];
18		}
19		return self;
20	}
21	
22	- (instancetype)initWithContentRect:(NSRect)contentRect styleMask:(NSWindowStyleMask)style backing:(NSBackingStoreType)backingStoreType defer:(BOOL)flag screen:(nullable NSScreen *)screen
23	{
24		self = [super initWithContentRect:contentRect styleMask:style backing:backingStoreType defer:flag screen:screen];
25		if (self) {
26			[self sharedInit];
27		}
28		return self;
29	}
30	
31	- (void)sharedInit
32	{
33		if (@available(macOS 11.0, *)) {
34			NSWindowStyleMask mask = [self styleMask];
35			mask |= NSWindowStyleMaskFullSizeContentView;
36			[self setStyleMask:mask];
37		} else {
38			[self setContentBorderThickness:22 forEdge:NSRectEdgeMinY];
39		}
40	}
41	
42	- (BOOL)validateMenuItem:(NSMenuItem *)menuItem
43	{
44		if ([menuItem action] == @selector(runToolbarCustomizationPalette:)) {
45			return NO;
46		}
47	
48		return [super validateMenuItem:menuItem];
49	}
50	
51	@end
52	
```

> AGENT

Verified and now I understand the real picture: **Tier 1's hard part is already built.** `BPMainWindowController` programmatically creates an `NSSplitViewController` with a `sidebarWithViewController:` item, `BPWindow` already sets `fullSizeContentView`, and `BPToolbar` already includes the sidebar tracking separator. The genuine gaps are just two window properties: **unified toolbar style** and **transparent titlebar** — neither is set anywhere.

That makes Tier 1 a small, low-risk change. Let me create the branch and add them where `fullSizeContentView` already lives.

> TOOL

tool_use Bash
id: toolu_01WT99L842U7buJvC4cNGLNK
```json
{
  "command": "git checkout -b tier1-tahoe-unified-toolbar && echo \"branch ready\"",
  "description": "Create Tier 1 branch off main"
}
```

> TOOL

tool_result
id: toolu_01WT99L842U7buJvC4cNGLNK
```
Switched to a new branch 'tier1-tahoe-unified-toolbar'
branch ready
```

> TOOL

tool_result
id: toolu_016cqJvFXazd83p8m5egPs8G
```
The file /home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/BPWindow.m has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_016cqJvFXazd83p8m5egPs8G
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/BPWindow.m",
  "old_string": "\tif (@available(macOS 11.0, *)) {\n\t\tNSWindowStyleMask mask = [self styleMask];\n\t\tmask |= NSWindowStyleMaskFullSizeContentView;\n\t\t[self setStyleMask:mask];\n\t} else {\n\t\t[self setContentBorderThickness:22 forEdge:NSRectEdgeMinY];\n\t}",
  "new_string": "\tif (@available(macOS 11.0, *)) {\n\t\tNSWindowStyleMask mask = [self styleMask];\n\t\tmask |= NSWindowStyleMaskFullSizeContentView;\n\t\t[self setStyleMask:mask];\n\n\t\t// Tahoe / Liquid Glass: merge the toolbar into the title bar and let the\n\t\t// full-height sidebar's material show through the title bar area.\n\t\tself.titlebarAppearsTransparent = YES;\n\t\tself.toolbarStyle = NSWindowToolbarStyleUnified;\n\t} else {\n\t\t[self setContentBorderThickness:22 forEdge:NSRectEdgeMinY];\n\t}"
}
```

> AGENT

Now build and launch to confirm it compiles and runs without crashing.

> TOOL

tool_use Bash
id: toolu_017nnsweEti939sBHARjjRQr
```json
{
  "command": "cd /home/<USER>/Developer/scottdensmore/cakebrew\nxcodebuild -workspace Cakebrew.xcworkspace -scheme Cakebrew -configuration Debug -destination 'platform=macOS' build > /tmp/cb_t1.log 2>&1; echo \"exit: $?\"; grep -E \"\\*\\* BUILD (SUCCEEDED|FAILED)\" /tmp/cb_t1.log; grep -nE \": error:|is only available\" /tmp/cb_t1.log | head\necho \"==== launch test ====\"; pkill -x Cakebrew 2>/dev/null; sleep 1\nAPP=\"/home/<USER>/Library/Developer/Xcode/DerivedData/Cakebrew-ejkvoljwklzjefduqadkgzlgzyoq/Build/Products/Debug/Cakebrew.app\"; open \"$APP\"; sleep 4\nif pgrep -x Cakebrew >/dev/null; then echo \"RUNNING (pid $(pgrep -x Cakebrew))\"; else echo \"NOT RUNNING - crash?\"; fi\necho \"==== any exceptions in log ====\"; log show --last 1m --predicate 'process == \"Cakebrew\"' 2>/dev/null | grep -iE \"exception|crash|unrecognized|assert\" | head",
  "description": "Build, launch, and check for crashes/exceptions",
  "timeout": 420000
}
```

> TOOL

tool_result
id: toolu_017nnsweEti939sBHARjjRQr
```
exit: 0
** BUILD SUCCEEDED ** [2.839 sec]
==== launch test ====
RUNNING (pid 44928)
==== any exceptions in log ====
```

> AGENT

Build succeeds, app launches and runs cleanly with no exceptions. Let me try to capture the window for visual confirmation.

> TOOL

tool_use Bash
id: toolu_0167cpeF4kHxrPT7jY6w8iUv
```json
{
  "command": "cd /tmp; rm -f cb_t1.png; osascript -e 'tell application \"Cakebrew\" to activate' 2>/dev/null; sleep 1; screencapture -x -o cb_t1.png 2>&1; if [ -f cb_t1.png ]; then echo \"captured $(du -h cb_t1.png | cut -f1)\"; else echo \"capture failed (screen recording permission)\"; fi",
  "description": "Attempt screenshot of the running app"
}
```

> TOOL

tool_result
id: toolu_0167cpeF4kHxrPT7jY6w8iUv
```
captured 7.9M
Shell cwd was reset to /home/<USER>/Developer/scottdensmore/cakebrew
```

> AGENT

A screenshot captured this time. Let me look at it to verify the unified toolbar / sidebar look.

> TOOL

tool_use Read
id: toolu_011fs7EDU2R77gDK1uVMxXfU
```json
{
  "file_path": "/tmp/cb_t1.png"
}
```

> TOOL

tool_result
id: toolu_011fs7EDU2R77gDK1uVMxXfU
```
{
  "type": "image",
  "source": {
    "type": "base64",
    "data": "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",
    "media_type": "image/jpeg"
  }
}
```

> AGENT

The app is clearly running with the sidebar (Installed/Outdated/All/Leaves/Repositories + Doctor/Update with badges), formula list, and search. It's small in the full-screen grab — let me crop to the window for a clearer view of the toolbar/sidebar treatment.

> TOOL

tool_use Bash
id: toolu_017FonaxnYGLf1ZFNA9NEzqG
```json
{
  "command": "cd /tmp\nB=$(osascript -e 'tell application \"System Events\" to tell process \"Cakebrew\" to get {position, size} of front window' 2>/dev/null)\necho \"bounds: $B\"\nif [ -n \"$B\" ]; then\n  X=$(echo $B | cut -d, -f1|tr -d ' '); Y=$(echo $B|cut -d, -f2|tr -d ' '); W=$(echo $B|cut -d, -f3|tr -d ' '); H=$(echo $B|cut -d, -f4|tr -d ' ')\n  rm -f cb_win.png; screencapture -x -R${X},${Y},${W},${H} cb_win.png 2>&1 && echo \"cropped win: $(du -h cb_win.png|cut -f1)\"\nelse\n  echo \"no bounds (accessibility blocked) - will enlarge window instead\"\nfi",
  "description": "Get window bounds and capture just the window"
}
```

> TOOL

tool_result
id: toolu_017FonaxnYGLf1ZFNA9NEzqG
```
bounds: 
no bounds (accessibility blocked) - will enlarge window instead
Shell cwd was reset to /home/<USER>/Developer/scottdensmore/cakebrew
```

> AGENT

Accessibility is blocked (can't query window bounds), but screen recording works. Let me crop the full screenshot to the window region for a clearer look.

> TOOL

tool_use Bash
id: toolu_01C1chMnpobow1yHiszjisLW
```json
{
  "command": "cd /tmp\nDIM=$(sips -g pixelWidth -g pixelHeight cb_t1.png 2>/dev/null | grep -E \"pixel\" | awk '{print $2}' | paste -sd'x' -)\necho \"image: $DIM\"\nW=$(sips -g pixelWidth cb_t1.png | awk '/pixelWidth/{print $2}'); H=$(sips -g pixelHeight cb_t1.png | awk '/pixelHeight/{print $2}')\n# Window occupies roughly center; crop x:11%..89%, y:14%..82%\nCX=$(echo \"$W*0.11/1\"|bc); CY=$(echo \"$H*0.13/1\"|bc); CW=$(echo \"$W*0.78/1\"|bc); CH=$(echo \"$H*0.70/1\"|bc)\necho \"crop offset ${CX},${CY} size ${CW}x${CH}\"\nrm -f cb_crop.png; sips -c $CH $CW --cropOffset $CY $CX cb_t1.png --out cb_crop.png >/dev/null 2>&1 && echo \"cropped: $(du -h cb_crop.png|cut -f1)\"",
  "description": "Crop screenshot to the window region"
}
```

> TOOL

tool_result
id: toolu_01C1chMnpobow1yHiszjisLW
```
image: 5120x2880
crop offset 563,374 size 3993x2016
cropped: 984K
Shell cwd was reset to /home/<USER>/Developer/scottdensmore/cakebrew
```

> TOOL

tool_use Read
id: toolu_01Ej7AcgYd4YTM76MauHvtfV
```json
{
  "file_path": "/tmp/cb_crop.png"
}
```

> TOOL

tool_result
id: toolu_01Ej7AcgYd4YTM76MauHvtfV
```
{
  "type": "image",
  "source": {
    "type": "base64",
    "data": "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",
    "media_type": "image/png"
  }
}
```

> AGENT

That's a clear, good-looking result. The sidebar renders natively — source-list style with SF Symbols, the count badges (Installed 126, Outdated 1, All 6392, Leaves 31, Repositories 2), and the modern blue rounded selection on "Installed". The content table and selected-formula panel look clean. Build succeeds, app runs, no exceptions.

Committing Tier 1 and opening a PR for your visual review (I won't auto-merge this one since it's a look change).

> TOOL

tool_use Bash
id: toolu_014Qfycrvktc7kdkBR8t9uCD
```json
{
  "command": "cd /home/<USER>/Developer/scottdensmore/cakebrew\ngit add Cakebrew/BPWindow.m && git commit -m \"$(cat <<'EOF'\nAdopt unified toolbar and transparent titlebar (Tahoe look)\n\nThe window already enabled full-size content and the sidebar is already an\nNSSplitViewController sidebar item, but the toolbar still used the legacy\nseparate title bar. Set toolbarStyle = unified and titlebarAppearsTransparent\nso the toolbar merges into the title bar and the full-height sidebar's\nmaterial reads through it — the signature macOS 26 look.\n\nCo-Authored-By: Claude Opus 4.7 (1M context) <<REDACTED_EMAIL>>\nEOF\n)\" && git push -u origin tier1-tahoe-unified-toolbar 2>&1 | tail -3",
  "description": "Commit and push Tier 1 change"
}
```

> TOOL

tool_result
id: toolu_014Qfycrvktc7kdkBR8t9uCD
```
[tier1-tahoe-unified-toolbar c27aa12] Adopt unified toolbar and transparent titlebar (Tahoe look)
 1 file changed, 5 insertions(+)
To https://github.com/scottdensmore/Cakebrew.git
 * [new branch]      tier1-tahoe-unified-toolbar -> tier1-tahoe-unified-toolbar
branch 'tier1-tahoe-unified-toolbar' set up to track 'origin/tier1-tahoe-unified-toolbar'.
```

> TOOL

tool_use Bash
id: toolu_01Sazb9oW4pM2Q1vXiGpVWnH
```json
{
  "command": "cd /home/<USER>/Developer/scottdensmore/cakebrew\ngh pr create --repo scottdensmore/Cakebrew --base main --head tier1-tahoe-unified-toolbar --title \"Adopt unified toolbar and transparent titlebar (Tahoe look)\" --body \"$(cat <<'EOF'\n## Summary\n**Phase 2 (Tier 1) of the Tahoe modernization.** Most of the signature look was already in place — `BPMainWindowController` builds an `NSSplitViewController` with a `sidebarWithViewController:` item, `BPWindow` enables `fullSizeContentView`, and `BPToolbar` already includes the sidebar tracking separator. The only missing pieces were the window chrome:\n\n- `window.toolbarStyle = NSWindowToolbarStyleUnified` — merges the toolbar into the title bar.\n- `window.titlebarAppearsTransparent = YES` — lets the full-height sidebar's material read through the title bar.\n\nBoth are set in `BPWindow.sharedInit` alongside the existing `fullSizeContentView` flag (macOS 11+ guarded; min target is 14).\n\n## Verification\n- [x] BUILD SUCCEEDED\n- [x] App launches, no exceptions; sidebar (source-list + SF Symbols + count badges) and content render correctly\n- [ ] **Please eyeball on your display:** unified toolbar merge, sidebar glass translucency, and whether the toolbar's sidebar **tracking separator** aligns to the divider.\n\n## Possible follow-up (not in this PR)\nThe split view controller is currently added as a *subview* of the window's content view rather than set as `window.contentViewController`. The system sidebar tracking separator aligns most reliably when the split view controller **is** the […]

> TOOL

tool_result
id: toolu_01Sazb9oW4pM2Q1vXiGpVWnH
```
https://github.com/scottdensmore/Cakebrew/pull/6
```

> AGENT

Here's where we are on the phased plan:

## Progress
- ✅ **Phase 1 — min OS macOS 14 Sonoma** — merged (`#5`).
- 🔍 **Tier 1 — Tahoe signature look** — **PR [#6](https://github.com/scottdensmore/Cakebrew/pull/6) open for your review.** The app is running right now so you can eyeball it.

**Notable discovery:** most of Tier 1 was *already implemented* in the codebase — `BPMainWindowController` already builds an `NSSplitViewController` with a real sidebar item, `BPWindow` already enables full-size content, and `BPToolbar` already wires the sidebar tracking separator. So instead of a big risky window rebuild, Tier 1 came down to two missing window properties: **unified toolbar** + **transparent titlebar**. Much lower risk than I'd budgeted.

The cropped screenshot confirmed the sidebar (source-list, SF Symbols, count badges, modern selection) and content render great.

## Your call on PR #6
Please take a look at the running app and check:
1. The toolbar merges into the title bar (unified look).
2. Sidebar glass translucency reads well in your appearance (light/dark).
3. Whether the toolbar's **sidebar tracking separator** lines up with the divider — if not, I have a small, clearly-scoped follow-up (set the split view controller as the window's `contentViewController`) noted in the PR. […]

> DEVELOPER

check the pr and see if there are any comments before you move on and address them. Once they are done you can merge and move to Tier 2

> AGENT

Let me check PR #6 for any review comments.

> TOOL

tool_use Bash
id: toolu_01X7ymSb6iuZmPv8HYELfgPs
```json
{
  "command": "cd /home/<USER>/Developer/scottdensmore/cakebrew\necho \"==== reviews on #6 ====\"; gh pr view 6 --repo scottdensmore/Cakebrew --json reviews --jq '.reviews[] | {user:.author.login, state:.state, at:.submittedAt}'\necho \"==== unresolved threads ====\"; gh api graphql -f query='query { repository(owner:\"scottdensmore\",name:\"Cakebrew\"){ pullRequest(number:6){ reviewThreads(first:50){ nodes{ id isResolved comments(first:5){ nodes{ databaseId author{login} path originalLine body } } } } } } }' --jq '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved==false) | {threadId:.id, comments:[.comments.nodes[]|{user:.author.login, path:.path, line:.originalLine, body:.body}]}'\necho \"(end)\"",
  "description": "Check PR #6 for reviews and unresolved threads"
}
```

> TOOL

tool_result
id: toolu_01X7ymSb6iuZmPv8HYELfgPs
```
==== reviews on #6 ====
{"at":"2026-05-26T05:26:17Z","state":"COMMENTED","user":"copilot-pull-request-reviewer"}
==== unresolved threads ====
{"comments":[{"body":"`MACOSX_DEPLOYMENT_TARGET` is set to 14.0 in the project, so the `@available(macOS 11.0, *)` check (and especially the `else` branch with `setContentBorderThickness:`) is now unreachable at runtime. Consider removing the availability branching (or updating it to match the actual deployment target) to avoid dead code and potential confusion about supported macOS versions.","line":44,"path":"Cakebrew/BPWindow.m","user":"copilot-pull-request-reviewer"}],"threadId":"PRRT_kwDOA4x9PM6EsHR4"}
(end)
```

> AGENT

PR #6 got an automatic Copilot review with one valid comment: with the min target now at 14.0, the `@available(macOS 11.0, *)` check and its `else` branch in `BPWindow.sharedInit` are dead code. That's exactly the kind of cleanup worth doing in the file I just touched. Let me remove the branching.

> TOOL

tool_use Edit
id: toolu_01Xu5pvj8YWCJp2hvdKqu7gs
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/BPWindow.m",
  "old_string": "\tif (@available(macOS 11.0, *)) {\n\t\tNSWindowStyleMask mask = [self styleMask];\n\t\tmask |= NSWindowStyleMaskFullSizeContentView;\n\t\t[self setStyleMask:mask];\n\n\t\t// Tahoe / Liquid Glass: merge the toolbar into the title bar and let the\n\t\t// full-height sidebar's material show through the title bar area.\n\t\tself.titlebarAppearsTransparent = YES;\n\t\tself.toolbarStyle = NSWindowToolbarStyleUnified;\n\t} else {\n\t\t[self setContentBorderThickness:22 forEdge:NSRectEdgeMinY];\n\t}",
  "new_string": "\tNSWindowStyleMask mask = [self styleMask];\n\tmask |= NSWindowStyleMaskFullSizeContentView;\n\t[self setStyleMask:mask];\n\n\t// Tahoe / Liquid Glass: merge the toolbar into the title bar and let the\n\t// full-height sidebar's material show through the title bar area.\n\tself.titlebarAppearsTransparent = YES;\n\tself.toolbarStyle = NSWindowToolbarStyleUnified;"
}
```

> TOOL

tool_result
id: toolu_01Xu5pvj8YWCJp2hvdKqu7gs
```
The file /home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/BPWindow.m has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Rebuilding to confirm, then I'll push, reply/resolve, and merge.

> TOOL

tool_use Bash
id: toolu_01ELSsy8sFxs1jJYTCBgfUPd
```json
{
  "command": "cd /home/<USER>/Developer/scottdensmore/cakebrew\nxcodebuild -workspace Cakebrew.xcworkspace -scheme Cakebrew -configuration Debug -destination 'platform=macOS' build > /tmp/cb_t1b.log 2>&1; echo \"exit: $?\"; grep -E \"\\*\\* BUILD (SUCCEEDED|FAILED)\" /tmp/cb_t1b.log; grep -nE \": error:|is only available\" /tmp/cb_t1b.log | head",
  "description": "Rebuild after dead-code removal",
  "timeout": 420000
}
```

> TOOL

tool_result
id: toolu_01ELSsy8sFxs1jJYTCBgfUPd
```
exit: 0
** BUILD SUCCEEDED ** [16.390 sec]
```

> AGENT

Build clean. Committing, then replying to and resolving the Copilot thread.

> TOOL

tool_use Bash
id: toolu_013FbLCettaig8dqBVEjy3AN
```json
{
  "command": "cd /home/<USER>/Developer/scottdensmore/cakebrew\ngit add Cakebrew/BPWindow.m && git commit -m \"$(cat <<'EOF'\nRemove dead macOS 11 availability branch in BPWindow\n\nWith the deployment target at macOS 14, the @available(macOS 11.0, *)\ncheck is always true and the pre-11 setContentBorderThickness: fallback\nis unreachable. Run the window setup unconditionally.\n\nCo-Authored-By: Claude Opus 4.7 (1M context) <<REDACTED_EMAIL>>\nEOF\n)\" && git push 2>&1 | tail -2\necho \"==== fetch comment id for reply ====\"\nCID=$(gh api repos/scottdensmore/Cakebrew/pulls/6/comments --jq '.[0].id'); echo \"comment id: $CID\"\ngh api repos/scottdensmore/Cakebrew/pulls/6/comments -F in_reply_to=$CID -f body=\"Fixed in the latest commit — removed the \\`@available(macOS 11.0, *)\\` wrapper and the unreachable \\`setContentBorderThickness:\\` fallback; the window setup now runs unconditionally (deployment target is macOS 14).\" --jq .id",
  "description": "Commit, push, and reply to the Copilot thread"
}
```

> TOOL

tool_result
id: toolu_013FbLCettaig8dqBVEjy3AN
```
[tier1-tahoe-unified-toolbar ae448f1] Remove dead macOS 11 availability branch in BPWindow
 1 file changed, 8 insertions(+), 12 deletions(-)
To https://github.com/scottdensmore/Cakebrew.git
   c27aa12..ae448f1  tier1-tahoe-unified-toolbar -> tier1-tahoe-unified-toolbar
==== fetch comment id for reply ====
comment id: 3301410226
3307823837
```

> AGENT

Reply posted. Now resolving the thread and merging PR #6.

> TOOL

tool_use Bash
id: toolu_01TH8HZxhaDD1Ex8GLqKS6qS
```json
{
  "command": "cd /home/<USER>/Developer/scottdensmore/cakebrew\necho \"==== resolve thread ====\"; gh api graphql -f query='mutation($id:ID!){resolveReviewThread(input:{threadId:$id}){thread{isResolved}}}' -f id=\"PRRT_kwDOA4x9PM6EsHR4\" --jq '.data.resolveReviewThread.thread.isResolved'\necho \"==== merge PR #6 ====\"; gh pr merge 6 --repo scottdensmore/Cakebrew --squash 2>&1 | tail -2\ngh pr view 6 --repo scottdensmore/Cakebrew --json state,mergeCommit --jq '{state, mergeCommit:.mergeCommit.oid}'\necho \"==== sync main + cleanup ====\"; git checkout main && git fetch origin --prune --quiet && git merge --ff-only origin/main 2>&1 | tail -1; git branch -D tier1-tahoe-unified-toolbar 2>&1; git push origin --delete tier1-tahoe-unified-toolbar 2>&1 | tail -1\necho \"==== main now ====\"; git log --oneline -3",
  "description": "Resolve thread, merge PR #6, sync main, clean up branch"
}
```

> TOOL

tool_result
id: toolu_01TH8HZxhaDD1Ex8GLqKS6qS
```
==== resolve thread ====
true
==== merge PR #6 ====
{"mergeCommit":"805b62b401f4e11dce62b8258413fd6a80e655b8","state":"MERGED"}
==== sync main + cleanup ====
Switched to branch 'main'
Your branch is up to date with 'origin/main'.
 1 file changed, 8 insertions(+), 7 deletions(-)
Deleted branch tier1-tahoe-unified-toolbar (was ae448f1).
 - [deleted]         tier1-tahoe-unified-toolbar
==== main now ====
805b62b Adopt unified toolbar and transparent titlebar (Tahoe look) (#6)
86766b8 Lower minimum deployment target to macOS 14 Sonoma (#5)
049f03e Add Entire CLI integration (#4)
```

> AGENT

**Tier 1 merged** (`#6` → main `805b62b`), thread resolved, branch cleaned up. The app shows the unified toolbar + full-height glass sidebar.

Now **Tier 2: toolbar & controls** (`NSSearchToolbarItem`, bordered SF-Symbol items, grouping). Let me read the full toolbar implementation to scope the exact changes.

> TOOL

tool_use Read
id: toolu_01FZGBeUZHdJwnHqVRGAMtyR
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/BPToolbar.m"
}
```

> TOOL

tool_result
id: toolu_01FZGBeUZHdJwnHqVRGAMtyR
```
1	//
2	//  BPToolbar.m
3	//  Cakebrew
4	//
5	//  Created by Marek Hrusovsky on 16/08/15.
6	//	Copyright (c) 2014 Bruno Philipe. All rights reserved.
7	//
8	//	This program is free software: you can redistribute it and/or modify
9	//	it under the terms of the GNU General Public License as published by
10	//	the Free Software Foundation, either version 3 of the License, or
11	//	(at your option) any later version.
12	//
13	//	This program is distributed in the hope that it will be useful,
14	//	but WITHOUT ANY WARRANTY; without even the implied warranty of
15	//	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
16	//	GNU General Public License for more details.
17	//
18	//	You should have received a copy of the GNU General Public License
19	//	along with this program.	If not, see <http://www.gnu.org/licenses/>.
20	//
21	
22	#import "BPToolbar.h"
23	#import "BPStyle.h"
24	
25	static NSString *kToolbarIdentifier = @"toolbarIdentifier";
26	
27	static NSString *kToolbarItemHomebrewUpdateIdentifier = @"toolbarItemHomebrewUpdate";
28	static NSString *kToolbarItemInformationIdentifier = @"toolbarItemInformation";
29	static NSString *kToolbarItemSearchIdentifier = @"toolbarItemSearch";
30	static NSString *kToolbarItemMultiActionIdentifier = @"toolbarItemMultiAction";
31	
32 […]

> AGENT

Tier 2 is also partly done: the search **already uses `NSSearchToolbarItem`** (line 298). The toolbar items, though, set their buttons to `setBordered:NO` (line 377) — so they miss Tahoe's new glass bordered-button treatment. The images come from `BPStyle`. Let me check whether `BPStyle` uses SF Symbols or old bitmaps — that decides the rest of Tier 2.

> TOOL

tool_use Bash
id: toolu_015XQwB6Xur1AFKuEV38KTNh
```json
{
  "command": "cd /home/<USER>/Developer/scottdensmore/cakebrew\necho \"==== BPStyle toolbar image methods ====\"; grep -nE \"toolbarImageFor|imageWithSystemSymbolName|imageNamed|toolbarSize|NSToolbarSizeMode\" Cakebrew/BPStyle.m",
  "description": "Inspect BPStyle toolbar image sources"
}
```

> TOOL

tool_result
id: toolu_015XQwB6Xur1AFKuEV38KTNh
```
==== BPStyle toolbar image methods ====
57:+ (NSToolbarSizeMode)toolbarSize
61:		return NSToolbarSizeModeSmall;
63:	return NSToolbarSizeModeDefault;
66:+ (NSImage *)toolbarImageForInstall
76:+ (NSImage *)toolbarImageForUninstall
86:+ (NSImage *)toolbarImageForTap
96:+ (NSImage *)toolbarImageForUntap
106:+ (NSImage *)toolbarImageForUpdate
116:+ (NSImage *)toolbarImageForMoreInformation
126:+ (NSImage *)toolbarImageForUpgrade
139:		return [NSImage imageWithSystemSymbolName:symbol accessibilityDescription:name];
141:		return [NSImage imageNamed:[NSString stringWithFormat:@"%@_flat", name]];
143:		return [NSImage imageNamed:[NSString stringWithFormat:@"%@.icns", name]];
```

> TOOL

tool_use Read
id: toolu_01VL1WdvWe23XjquEfPCjUL2
```json
{
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/BPStyle.m",
  "offset": 55,
  "limit": 95
}
```

> TOOL

tool_result
id: toolu_01VL1WdvWe23XjquEfPCjUL2
```
55	#pragma mark Toolbar
56	
57	+ (NSToolbarSizeMode)toolbarSize
58	{
59		if (self.isFlat)
60		{
61			return NSToolbarSizeModeSmall;
62		}
63		return NSToolbarSizeModeDefault;
64	}
65	
66	+ (NSImage *)toolbarImageForInstall
67	{
68		static NSImage *image;
69		if (!image) {
70			image = [self appropriateIconForToolbarWithName:@"download" orSymbol:@"plus.circle.fill"];
71		}
72		
73		return image;
74	}
75	
76	+ (NSImage *)toolbarImageForUninstall
77	{
78		static NSImage *image;
79		if (!image) {
80			image = [self appropriateIconForToolbarWithName:@"delete" orSymbol:@"xmark.circle.fill"];
81		}
82		
83		return image;
84	}
85	
86	+ (NSImage *)toolbarImageForTap
87	{
88		static NSImage *image;
89		if (!image) {
90			image = [self appropriateIconForToolbarWithName:@"download" orSymbol:@"plus.circle.fill"];
91		}
92		
93		return image;
94	}
95	
96	+ (NSImage *)toolbarImageForUntap
97	{
98		static NSImage *image;
99		if (!image) {
100			image = [self appropriateIconForToolbarWithName:@"delete" orSymbol:@"xmark.circle.fill"];
101		}
102		
103		return image;
104	}
105	
106	+ (NSImage *)toolbarImageForUpdate
107	{
108		static NSImage *image;
109		if (!image) {
110			image = [self appropriateIconForToolbarWithName:@"reload" orSymbol:@"arrow.triangle.2.circlepath.circle.fill"];
111		}
112		
113		return image;
114	}
115	
116	+ (NSImage *)toolbarImageForMoreInformation
117	{
118		static NSImage *image;
119		if (!image) {
120			image = [self appropriateIconForToolbarWithName:@"label" orSymbol:@"info.circle.fill"];
121		}
122		
123		return […]

> AGENT

Tier 2 is also mostly in place: search **already uses `NSSearchToolbarItem`**, and `BPStyle` **already returns SF Symbols** for all toolbar images. The genuine gap is that the toolbar buttons are built as **borderless** custom buttons (`setBordered:NO`, line 377) with an oversized 24pt symbol — so they miss Tahoe's glass bordered-button look. Since screenshotting works now, I'll make them bordered, right-size the symbol, then look and iterate.

> TOOL

tool_use Bash
id: toolu_01ESGsqA3VzYBU22dJxBBpC2
```json
{
  "command": "git checkout -b tier2-tahoe-toolbar-buttons && echo ready",
  "description": "Create Tier 2 branch"
}
```

> TOOL

tool_result
id: toolu_01ESGsqA3VzYBU22dJxBBpC2
```
Switched to a new branch 'tier2-tahoe-toolbar-buttons'
ready
```

> TOOL

tool_result
id: toolu_01T2P1ijYeWPbFngZhxyU8kt
```
The file /home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/BPToolbar.m has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01T2P1ijYeWPbFngZhxyU8kt
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Developer/scottdensmore/cakebrew/Cakebrew/BPToolbar.m",
  "old_string": "\tNSButton *button = [NSButton buttonWithImage:image target:target action:action];\n\t[button setBezelStyle:NSBezelStyleRegularSquare];\n\t[button setBordered:NO];\n\t[button setTranslatesAutoresizingMaskIntoConstraints:NO];\n\tif (@available(macOS 11, *)) {\n\t\t[button setSymbolConfiguration:[NSImageSymbolConfiguration configurationWithPointSize:24\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t  weight:NSFontWeightMedium\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t   scale:NSImageSymbolScaleMedium]];\n\t}\n\t[button setImageScaling:NSImageScaleProportionallyUpOrDown];\n\treturn button;",
  "new_string": "\tNSButton *button = [NSButton buttonWithImage:image target:target action:action];\n\t// Bordered so the toolbar buttons pick up the macOS 26 Liquid Glass capsule.\n\t[button setBezelStyle:NSBezelStyleTexturedRounded];\n\t[button setBordered:YES];\n\t[button setTranslatesAutoresizingMaskIntoConstraints:NO];\n\t[button setSymbolConfiguration:[NSImageSymbolConfiguration configurationWithPointSize:15\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t  weight:NSFontWeightRegular\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t   scale:NSImageSymbolScaleMedium]];\n\t[button setImageScaling:NSImageScaleProportionallyDown];\n\treturn button;"
}
```

> TOOL

tool_use Bash
id: toolu_01FuVMvm9NVEjS71npciewN1
```json
{
  "command": "cd /home/<USER>/Developer/scottdensmore/cakebrew\nxcodebuild -workspace Cakebrew.xcworkspace -scheme Cakebrew -configuration Debug -destination 'platform=macOS' build > /tmp/cb_t2.log 2>&1; echo \"exit: $?\"; grep -E \"\\*\\* BUILD (SUCCEEDED|FAILED)\" /tmp/cb_t2.log; grep -nE \": error:\" /tmp/cb_t2.log | head\necho \"==== relaunch ====\"; pkill -x Cakebrew 2>/dev/null; sleep 1\nopen \"/home/<USER>/Library/Developer/Xcode/DerivedData/Cakebrew-ejkvoljwklzjefduqadkgzlgzyoq/Build/Products/Debug/Cakebrew.app\"; sleep 4\npgrep -x Cakebrew >/dev/null && echo \"running\" || echo \"NOT running\"",
  "description": "Build and relaunch with bordered toolbar buttons",
  "timeout": 420000
}
```

> TOOL

tool_result ERROR
id: toolu_01FuVMvm9NVEjS71npciewN1
```
Tool permission request failed: Error: Tool permission stream closed before response received
```

> AGENT

No response requested.

> DEVELOPER

have all the local changes been merged into this branch?

> AGENT

Let me check the actual state — I don't want to guess.

> TOOL

tool_use Bash
id: toolu_017f6rtro1w8VQkguYH2Q6Ka
```json
{
  "command": "cd /home/<USER>/Developer/scottdensmore/cakebrew\necho \"==== current branch ====\"; git branch --show-current\necho \"==== status ====\"; git status -sb | head -15\necho \"==== commits vs main ====\"; git log --oneline main..HEAD 2>/dev/null\necho \"==== diff vs main ====\"; git diff --stat main..HEAD; git diff --stat\necho \"==== main vs origin/main ====\"; git fetch origin --quiet 2>&1; git rev-parse --short main origin/main",
  "description": "Check current branch, working tree, commits ahead of main, and remote sync"
}
```

> TOOL

tool_result ERROR
id: toolu_017f6rtro1w8VQkguYH2Q6Ka
```
Exit code 128
==== current branch ====
tier2-tahoe-toolbar-buttons
==== status ====
## tier2-tahoe-toolbar-buttons
 M Cakebrew/BPToolbar.m
==== commits vs main ====
==== diff vs main ====
 Cakebrew/BPToolbar.m | 15 +++++++--------
 1 file changed, 7 insertions(+), 8 deletions(-)
==== main vs origin/main ====
fatal: Needed a single revision
```

> AGENT

No — the Tier 2 edit is still uncommitted in the working tree, and the branch has nothing on it yet.

Here's the actual state:

- **Current branch:** `tier2-tahoe-toolbar-buttons`
- **Working tree:** `Cakebrew/BPToolbar.m` has uncommitted modifications (the bordered/glass toolbar button change — `setBordered:YES`, retuned symbol config). Status shows ` M` = modified, not staged, not committed.
- **Commits ahead of `main`:** none. The branch tip is identical to `main`; the only difference is the uncommitted working-tree change.
- **Not pushed to origin** (no upstream set).
- The build right after that edit was interrupted (the tool permission error from the last session), so I never confirmed it compiled or screenshotted the result.

For context, what *is* already on `main` and synced:
- ✅ **Phase 1** — min OS macOS 14 Sonoma (`#5`)
- ✅ **Tier 1** — unified toolbar + transparent titlebar (`#6`)

What's still in flight:
- 🟡 **Tier 2** — the BPToolbar.m bordered-buttons edit, **uncommitted** in the working tree.

Want me to pick up where we left off — build, launch, screenshot to verify, then commit/push/PR the Tier 2 change?