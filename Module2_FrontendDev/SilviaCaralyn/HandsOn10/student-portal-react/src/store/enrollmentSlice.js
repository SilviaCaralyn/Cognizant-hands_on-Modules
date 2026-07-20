import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { getAllCourses } from '../api/courseApi.js'

// Step 143: async thunk wrapping the centralized API layer
export const fetchAllCourses = createAsyncThunk(
  'courses/fetchAll',
  async (_, { rejectWithValue }) => {
    try {
      return await getAllCourses()
    } catch (err) {
      return rejectWithValue(err.message || 'Failed to fetch courses')
    }
  }
)

const enrollmentSlice = createSlice({
  name: 'enrollment',
  initialState: {
    enrolledCourses: [],
    courses: [],
    loading: false,
    error: null,
  },
  reducers: {
    enroll(state, action) {
      const course = action.payload
      const alreadyEnrolled = state.enrolledCourses.some((c) => c.id === course.id)
      if (!alreadyEnrolled) state.enrolledCourses.push(course)
    },
    unenroll(state, action) {
      const courseId = action.payload
      state.enrolledCourses = state.enrolledCourses.filter((c) => c.id !== courseId)
    },
  },
  // Step 144: handle the three thunk lifecycle actions
  extraReducers: (builder) => {
    builder
      .addCase(fetchAllCourses.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchAllCourses.fulfilled, (state, action) => {
        state.courses = action.payload
        state.loading = false
      })
      .addCase(fetchAllCourses.rejected, (state, action) => {
        state.error = action.payload || 'Something went wrong'
        state.loading = false
      })
  },
})

export const { enroll, unenroll } = enrollmentSlice.actions

// Step 146: selectors — components never touch store shape directly
export const selectCourses = (state) => state.enrollment.courses
export const selectCoursesLoading = (state) => state.enrollment.loading
export const selectCoursesError = (state) => state.enrollment.error
export const selectEnrolledCourses = (state) => state.enrollment.enrolledCourses
export const selectEnrolledCount = (state) => state.enrollment.enrolledCourses.length

export default enrollmentSlice.reducer
