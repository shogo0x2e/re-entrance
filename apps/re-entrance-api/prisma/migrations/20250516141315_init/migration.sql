-- CreateEnum
CREATE TYPE "JobStatus" AS ENUM ('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED');

-- CreateTable
CREATE TABLE "Feature" (
    "id" TEXT NOT NULL,
    "timestamp" INTEGER NOT NULL,
    "vectorId" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Feature_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Clip" (
    "id" TEXT NOT NULL,
    "filename" TEXT NOT NULL,
    "path" TEXT NOT NULL,
    "recordedAt" TIMESTAMP(3) NOT NULL,
    "duration" INTEGER NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Clip_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "SceneJob" (
    "id" TEXT NOT NULL,
    "status" "JobStatus" NOT NULL DEFAULT 'PENDING',
    "error" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "SceneJob_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "ClipSegment" (
    "id" TEXT NOT NULL,
    "jobId" TEXT NOT NULL,
    "clipId" TEXT NOT NULL,
    "startSeconds" INTEGER NOT NULL,
    "endSeconds" INTEGER NOT NULL,
    "order" INTEGER NOT NULL,

    CONSTRAINT "ClipSegment_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Scene" (
    "id" TEXT NOT NULL,
    "clipId" TEXT NOT NULL,
    "jobId" TEXT NOT NULL,
    "featureId" TEXT NOT NULL,
    "filename" TEXT NOT NULL,
    "path" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Scene_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE INDEX "Feature_timestamp_idx" ON "Feature"("timestamp");

-- CreateIndex
CREATE INDEX "Clip_recordedAt_idx" ON "Clip"("recordedAt");

-- CreateIndex
CREATE INDEX "ClipSegment_jobId_order_idx" ON "ClipSegment"("jobId", "order");

-- CreateIndex
CREATE INDEX "ClipSegment_clipId_idx" ON "ClipSegment"("clipId");

-- CreateIndex
CREATE UNIQUE INDEX "Scene_jobId_key" ON "Scene"("jobId");

-- CreateIndex
CREATE UNIQUE INDEX "Scene_featureId_key" ON "Scene"("featureId");

-- AddForeignKey
ALTER TABLE "ClipSegment" ADD CONSTRAINT "ClipSegment_jobId_fkey" FOREIGN KEY ("jobId") REFERENCES "SceneJob"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "ClipSegment" ADD CONSTRAINT "ClipSegment_clipId_fkey" FOREIGN KEY ("clipId") REFERENCES "Clip"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Scene" ADD CONSTRAINT "Scene_clipId_fkey" FOREIGN KEY ("clipId") REFERENCES "Clip"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Scene" ADD CONSTRAINT "Scene_jobId_fkey" FOREIGN KEY ("jobId") REFERENCES "SceneJob"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Scene" ADD CONSTRAINT "Scene_featureId_fkey" FOREIGN KEY ("featureId") REFERENCES "Feature"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
