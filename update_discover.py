import sys
import io

with open(r'c:\Users\Woundex\Desktop\norest\BooksLibrary\src\pages\User\Discover.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Rate state
content = content.replace('const [Category, setCategory] = useState("All");', 'const [Category, setCategory] = useState("All");\n    const [Rate, setRate] = useState("All");')

# 2. Add rate to SearchParams default state
content = content.replace('useState({ query: "", author: "", category: "All", sortOrder: "desc" });', 'useState({ query: "", author: "", category: "All", rate: "All", sortOrder: "desc" });')

# 3. Add rate to handleSearchSubmit
content = content.replace('setSearchParams({ query: SearchQuery, author: SearchAuthor, category: Category, sortOrder: SortOrder });', 'setSearchParams({ query: SearchQuery, author: SearchAuthor, category: Category, rate: Rate, sortOrder: SortOrder });')

# 4. Add rate handling to fetchBooks
fetch_old = """                } else if (SearchParams.category !== "All") {
                    response = await BooksApi.getBooksByCategory(SearchParams.category, params);
                } else {"""
fetch_new = """                } else if (SearchParams.category !== "All") {
                    response = await BooksApi.getBooksByCategory(SearchParams.category, params);
                } else if (SearchParams.rate !== "All") {
                    response = await BooksApi.getBooksByRate(Number(SearchParams.rate), params);
                } else {"""
content = content.replace(fetch_old, fetch_new)

# 5. Add Rate dropdown UI
dropdown_old = """                                    <label className="text-xs font-bold uppercase tracking-wider text-gray-500 dark:text-zinc-400 ml-1">Category</label>"""
dropdown_new = """                                    <label className="text-xs font-bold uppercase tracking-wider text-gray-500 dark:text-zinc-400 ml-1">Minimum Rate</label>
                                    <div className="relative">
                                        <select 
                                            value={Rate}
                                            onChange={(e) => setRate(e.target.value)}
                                            className='bg-gray-50 dark:bg-zinc-900/50 border border-gray-200 dark:border-zinc-700 text-gray-700 dark:text-zinc-300 rounded-xl px-4 py-3 appearance-none focus:outline-none focus:border-orange-500 focus:ring-2 focus:ring-orange-500/20 cursor-pointer font-medium transition-all'>
                                            <option value="All">All Ratings</option>
                                            <option value="5">5 Stars</option>
                                            <option value="4">4+ Stars</option>
                                            <option value="3">3+ Stars</option>
                                            <option value="2">2+ Stars</option>
                                            <option value="1">1+ Stars</option>
                                        </select>
                                        <ChevronDown className="absolute right-4 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none" />
                                    </div>
                                </div>
                                <div className="flex flex-col gap-2">
                                    <label className="text-xs font-bold uppercase tracking-wider text-gray-500 dark:text-zinc-400 ml-1">Category</label>"""

content = content.replace(dropdown_old, dropdown_new)

with open(r'c:\Users\Woundex\Desktop\norest\BooksLibrary\src\pages\User\Discover.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated Discover.tsx')
